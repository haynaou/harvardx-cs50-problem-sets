#include <stdio.h>
#include <cs50.h>
#include <math.h>
#include <ctype.h>
# include <string.h>

// declare functions
int numbers_of_letters(string text);
int numbers_of_words(string text);
int numbers_of_sentences(string text);
int coleman_liau_index(int letters, int words, int sentences);


int main(void)
{
    // Get user text
    string text = get_string("Text: ");

    // Calculate number of letters in text
    int letters = numbers_of_letters(text);

    // Calculate number of words in text
    int words = numbers_of_words(text);

    // Calculate number of sentences in text
    int sentences = numbers_of_sentences(text);

    // Calculate coleman index
    int index = coleman_liau_index(letters, words, sentences);

    // printf("Letters %i, Words %i, Sentences %i, index %i\n", letters, words, sentences, index);

    // Prints result grade of the texts
    if (index < 1)
    {
        printf("Before Grade %i\n", 1);
    }
    else if (index > 16)
    {
        printf("Grade %i+\n", 16);
    }
    else if ((index > 1) || (index >= 16)) 
    {
        printf("Grade %i\n", index);
    }
}

// function that counts letters including upper and lower case
int numbers_of_letters(string text)
{
    int letters_counter = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (isalpha(text[i]))
        {
            letters_counter++;
        }
    }

    return letters_counter;
}

// function that counts words, separated by space, words +1 for the last words, sentence with mutltiple words
int numbers_of_words(string text)
{
    int words_counter = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] == ' ' && text[i + 1] != ' ')
        {
            words_counter++;
        }
    }
    return words_counter + 1;

}

// function that counts sentences, separated by punctiation marks, .,!,? not a ,
int numbers_of_sentences(string text)
{
    int sentence_counter = 0;
    for (int i = 0; text[i] != '\0'; i++)
    {
        if (text[i] != ' ' && text[i + 1] == '.')
        {
            sentence_counter++;
        }
        else if (text[i] != ' ' && text[i + 1] == '!')
        {
            sentence_counter++;
        }
        else if (text[i] != ' ' && text[i + 1] == '?')
        {
            sentence_counter++;
        }
    }
    return sentence_counter;

}

// output is Coleman-Liau index of the text Grade X (16+ if >16, before 1 if less than 1)
int coleman_liau_index(int letters, int words, int sentences)
{
    float L = (float)(letters * 100) / words;
    float S = (float)(sentences * 100) / words;
    int index = round((0.0588 * L) - (0.296 * S) - 15.8);
    return index;
}
