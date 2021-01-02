from cs50 import get_string
import re

def main():
    # Get user text
    text = get_string("Text: ")
    
    # Calculate number of letters in text
    letters = sum([i.isalpha() for i in text]) 

    # Calculate number of words in text
    words = len(text.split(' '))

    # Calculate number of sentences in text,
    # by looking at any non white-space characters followed by punctiation marks ".", "!" or "?" 
    sentences = len(re.findall("[^ ][\.|?|!]", text))

    # Calculate coleman index
    index = coleman_liau_index(letters, words, sentences)

    #  Prints result grade of the texts
    if (index < 1):
        print("Before Grade 1")
    elif (index > 16):
        print("Grade 16+")
    elif ((index > 1) or (index >= 16)):
        print(f"Grade {index}")


#  output is Coleman-Liau index of the text Grade X (16+ if >16, before 1 if less than 1)
def coleman_liau_index(letters, words, sentences):
    L = (letters * 100) / words
    S = (sentences * 100) / words
    index = round((0.0588 * L) - (0.296 * S) - 15.8)
    return index
    
main()