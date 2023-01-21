import wikipedia


BLACK_LIST = ["who", "what", "when", "where", "why", "how", "is", "a", "the", "your", "of", "that", "you", "could",
              "have", "would", "should", "it", "be", "and", "if", "an", "to", "for", "do", "were"]


def remove_words(input_str: str) -> str:
    """Takes in a string and removes words on blacklist."""
    output_str = ""
    for word in input_str.split(" "):
        word = word.replace("?", "")
        if word not in BLACK_LIST:
            output_str += word
            output_str += " "
    return output_str


def wiki_search(query: str):
    """Takes in a question string and gets an answer from google."""
    key_words = remove_words(query)
    # print("Key words:", key_words)
    query = wikipedia.search(key_words, results=5)
    # print("Top wiki articles:", query)
    for q in query:
        try:  # Fixes occasional wiki search page not found error
            answer = wikipedia.summary(q, sentences=1)  # TODO: possibly extend on a conversation about a question (>1)
            break
        except:
            pass
    return answer


print("INPUT WARNING: '?' forces a query search for an answer.\n"
      "\tContractions will destroy input information (e.g. what's).\n")

while True:
    user_input = input("User: ").lower()
    if "?" in user_input:  # If question, wiki answer
        output = wiki_search(user_input)
    else:  # If not question, repeat user input filtered
        # TODO: Implement non question conversation replies
        output = "Non question reply not implemented."
    print("\nChatter:", output, "\n")
