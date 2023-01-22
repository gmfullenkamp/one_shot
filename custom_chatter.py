from PyDictionary import PyDictionary

DICT = PyDictionary()


def remove_from_str(in_str: str, black_list: list) -> str:
    """Removes strings and characters from the input string."""
    for w in black_list:
        in_str = in_str.replace(w, "")
    return in_str


def definition_search(in_str: str):
    """Takes in a 'Define...' string and outputs the definition"""
    key_words = remove_from_str(in_str.lower(), ["define ", "?", ".", ",", "'"])  # Removes extraneous words and chars
    answer = ""
    if " " in key_words:  # Retrieves the first word definition if multiple are given
        key_words = key_words.split(" ")[0]
        answer = "Multiple words inputted. Defining " + key_words + ". "
        meaning = DICT.meaning(key_words)
    else:
        meaning = DICT.meaning(key_words, disable_errors=True)
    if meaning is not None:
        for m in meaning.keys():  # Goes through the definitions and adds them all to the answer
            for sm in meaning[m]:
                answer += (m + ": " + sm + ". \n\t")
        answer = answer[:-2]  # Removes the last return '\n'
    else:
        answer = "'" + key_words + "' isn't a real word."
    # more_answer =  # TODO: Possibly have synonym and other word based information
    return answer


# print("INPUT WARNING: \n")

while True:
    user_input = input("User: ").lower()
    if "define" in user_input:
        output = definition_search(user_input)
    else:
        output = "Not implemented error. Try using define."
    print("\nChatter:", output, "\n")
