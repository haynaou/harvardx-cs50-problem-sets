// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include "dictionary.h"
#include <string.h>
#include <stdlib.h>
#include <strings.h>
#include <ctype.h>

// Function protoypes
char *strtolower(const char *str);

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 143091;

// Hash table
node *table[N];

// Count the words in dictionary
int word_counter = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Hash word
    int index = hash(word);

    // Check if word is in dictionary
    node *p = table[index];

    if (p == NULL)
    {
        return false;
    }

    while (strcasecmp(p->word, word) != 0 && p->next != NULL)
    {
        p = p->next;
    }

    if (strcasecmp(p->word, word) == 0)
    {
        return true;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    char * wordlower = strtolower(word);
    // it's important to choose a big number for the type of sum (long)
    // to hold the sum of the characters without overflow.
    long sum = 0;

    // Loop and sum ASCII code for all characters of the string s
    // until we reach end of character '\0'
     for (int i = 0; wordlower[i] != '\0'; i++)
     {
     // s[i] is char, so cast it to int
     // to get the int representation of it (ASCII code).
        sum += (int)wordlower[i];
     }

     free(wordlower);
    // Our sum might exceed N, so we need to apply % N
    // to contain it between 0 & N-1
    return sum % N;

}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        printf("Invalid dictionary");
        return false;
    }

    // Loop over words in dictionary provided in load into hash table
    char word[LENGTH];

    while (fscanf(dict, "%s", word) != EOF)
    {
       // Create a new node
       node *n = malloc(sizeof(node));
       if (n == NULL)
       {
           return false;
       }

       // Copy the word into the node
       strcpy(n->word, word);
       n->next = NULL;

       // Increment word counter
       word_counter++;

       // Insert word into Hash table
       int index = hash(word);
       if (table[index] == NULL)
       {
           table[index] = n;
       }
       else
       {
           node *p = table[index];

           while (p->next != NULL)
           {
               p = p->next;
           }
           p->next = n;

       }
    }

    fclose(dict);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return word_counter;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // Create 2 pointers
    node *p;
    node *temp;

    for (int i = 0; i < N; i++)
    {
        p = table[i];

        if (p != NULL)
        {
            while (p != NULL)
            {
                temp = p->next;
                free(p);
                p = temp;

            }
        }

    }

    return true;
}


// string to lower case

char *strtolower(const char *str)
{
    char *lower = malloc(LENGTH+1);
    for(int i = 0; str[i] != '\0'; i++)
    {
        lower[i] = tolower(str[i]);
    }

    return lower;

}