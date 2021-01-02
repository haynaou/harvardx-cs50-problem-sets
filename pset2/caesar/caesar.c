#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>


//Functions declaration:
bool is_invalid_key(string argv);
int get_key(int argc, string argv[]);
string cipher(string plaintext, int key);


// Get user key
int main(int argc, string argv[])
{
    // Check if key is valid
    int key = get_key(argc, argv);

    // Check bad key case
    if (key == -1)
    {
        return 1;
    }
    
    // Get user input and cipher
    string plaintext = get_string("Plaintext: ");
    string ciphertext = cipher(plaintext, key);
    printf("ciphertext: %s\n", ciphertext);
    
    return 0;
}

// fget_key checks if key is valid
// returns -1 if key is invalid, otherwise returns key
int get_key(int argc, string argv[])
{
    // Number of arguments provided
    int len_args = argc - 1;

    // If no command-line provided or more than 2 commands are provided return -1
    if (len_args == 0 || len_args >= 2 || is_invalid_key(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return -1;
    }

    // if key provided is digit, cast to int and return key
    return atoi(argv[1]);
}


// is_invalid_key checks if key is non digit
bool is_invalid_key(string argv)
{
    bool valid_key = true;
    for (int i = 0; argv[i] != '\0'; i++)
    {
        if (!isdigit(argv[i]))
        {
            valid_key = false;
            break;
        }
    }
    return !valid_key;
}

// cipher encrypts the given plain text with the
// provided key using Caesar algorithm
// returns cipher text
string cipher(string plaintext, int key)
{
    int n = strlen(plaintext);
    string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string ciphertext = malloc((n + 1) * sizeof(char));

    for (int i = 0; i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            // Get the index of the plaintext character in the alphabet string by
            // converting the character to upper case and shiffting its ASCII 
            // code index by 65 in order to get a value between 0 and strlen(alphabets)
            int plain_char_index = toupper(plaintext[i]) - 65;
            
            // Get ciphered character index
            int ciphered_char_index = (plain_char_index + key) % 26;
            
            // Make the case of the ciphered character match the plaintext case
            if (islower(plaintext[i]))
            {
                ciphertext[i] = tolower(alphabet[ciphered_char_index]);
            }
            else
            {
                ciphertext[i] = alphabet[ciphered_char_index];
            }
        }
        // keep the character as is if it's not alpha
        else
        {
            ciphertext[i] = plaintext[i];
        }
        
    }

    return ciphertext;
}
