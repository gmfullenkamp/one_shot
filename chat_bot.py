import numpy as np
import os
import re
import tensorflow as tf
import tensorflow_datasets as tfds
from tqdm import tqdm

# Load dataset
print("Loading Dataset...")
squad_ds = tfds.load("squad")
train_ds = squad_ds["train"]
validation_ds = squad_ds["validation"]

# Runs through the entire dataset and adds all words to the vocab tokenizer
questions = []
answers = []
print("Iterating through train dataset...")
# TODO: Train using entire dataset on home machine
for sample in tqdm(train_ds.take(8000).as_numpy_iterator()):
    answers.append(sample["answers"]["text"][0].decode("utf-8"))
    questions.append(sample["question"].decode("utf-8"))
print("Iterating through validation dataset...")
for sample in tqdm(validation_ds.take(2000).as_numpy_iterator()):
    answers.append(sample["answers"]["text"][0].decode("utf-8"))
    questions.append(sample["question"].decode("utf-8"))
tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts(questions + answers)
VOCAB_SIZE = len(tokenizer.word_index) + 1
print("VOCAB SIZE : {}".format(VOCAB_SIZE))

vocab = []
for word in tokenizer.word_index:
    vocab.append(word)


def tokenize(sentences):
    tokens_list = []
    vocabulary = []
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub("[^a-zA-Z]", ' ', sentence)
        tokens = sentence.split()
        vocabulary += tokens
        tokens_list.append(tokens)
    return tokens_list, vocabulary


# encoder_input_data
tokenized_questions = tokenizer.texts_to_sequences(questions)
maxlen_questions = max([len(x) for x in tokenized_questions])
padded_questions = tf.keras.preprocessing.sequence.pad_sequences(tokenized_questions, maxlen=maxlen_questions,
                                                                 padding="post")
encoder_input_data = np.array(padded_questions)
print("Encoder input shape:", encoder_input_data.shape, "\nQuestions max length:", maxlen_questions)

# decoder_input_data
tokenized_answers = tokenizer.texts_to_sequences(answers)
maxlen_answers = max([len(x) for x in tokenized_answers])
padded_answers = tf.keras.preprocessing.sequence.pad_sequences(tokenized_answers, maxlen=maxlen_answers, padding="post")
decoder_input_data = np.array(padded_answers)
print("Decoder input shape:", decoder_input_data.shape, "\nAnswers max length:", maxlen_answers)

# decoder_output_data
tokenized_answers = tokenizer.texts_to_sequences(answers)
for i in range(len(tokenized_answers)):
    tokenized_answers[i] = tokenized_answers[i][1:]
padded_answers = tf.keras.preprocessing.sequence.pad_sequences(tokenized_answers, maxlen=maxlen_answers, padding="post")
onehot_answers = tf.keras.utils.to_categorical(padded_answers, VOCAB_SIZE)
decoder_output_data = np.array(onehot_answers)
print("Decoder output shape:", decoder_output_data.shape)

print("Loading seq2seq model...")
encoder_inputs = tf.keras.layers.Input(shape=(maxlen_questions,))
encoder_embedding = tf.keras.layers.Embedding(VOCAB_SIZE, 200, mask_zero=True)(encoder_inputs)
encoder_outputs, state_h, state_c = tf.keras.layers.LSTM(200, return_state=True)(encoder_embedding)
encoder_states = [state_h, state_c]

decoder_inputs = tf.keras.layers.Input(shape=(maxlen_answers,))
decoder_embedding = tf.keras.layers.Embedding(VOCAB_SIZE, 200, mask_zero=True)(decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM(200, return_state=True, return_sequences=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = tf.keras.layers.Dense(VOCAB_SIZE, activation=tf.keras.activations.softmax)
output = decoder_dense(decoder_outputs)

model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output)
model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss="categorical_crossentropy")
model.summary()

# Train model
model_path = os.path.join(os.getcwd(), "model.h5")
if not os.path.exists(model_path):
    model.fit([encoder_input_data, decoder_input_data], decoder_output_data, batch_size=50, epochs=150)
    model.save("model.h5")
else:
    model.load_weights(model_path)


def make_inference_models():
    encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

    decoder_state_input_h = tf.keras.layers.Input(shape=(200,))
    decoder_state_input_c = tf.keras.layers.Input(shape=(200,))

    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_embedding, initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = tf.keras.models.Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states)

    return encoder_model, decoder_model


def str_to_tokens(sentence: str):
    words = sentence.lower().split()
    tokens_list = list()
    for wrd in words:
        tokens_list.append(tokenizer.word_index[wrd])
    return tf.keras.preprocessing.sequence.pad_sequences([tokens_list], maxlen=maxlen_questions, padding="post")


# Conversation time!
enc_model, dec_model = make_inference_models()

for _ in range(10):
    states_values = enc_model.predict(str_to_tokens(input("Enter question: ")))
    empty_target_seq = np.zeros((1, 1))
    empty_target_seq[0, 0] = tokenizer.word_index["start"]
    stop_condition = False
    decoded_translation = ''
    while not stop_condition:
        dec_outputs, h, c = dec_model.predict([empty_target_seq] + states_values)
        sampled_word_index = np.argmax(dec_outputs[0, -1, :])
        sampled_word = None
        for word, index in tokenizer.word_index.items():
            if sampled_word_index == index:
                decoded_translation += " {}".format(word)
                sampled_word = word

        if sampled_word == "end" or len(decoded_translation.split()) > maxlen_answers:
            stop_condition = True

        empty_target_seq = np.zeros((1, 1))
        empty_target_seq[0, 0] = sampled_word_index
        states_values = [h, c]

    print(decoded_translation)
