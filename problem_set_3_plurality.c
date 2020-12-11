#include <cs50.h>
#include <stdio.h>
#include <strings.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);
void sort(candidate *array, int size);
      
int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
// returns true if candidate candidate is found, otherwise false
bool vote(string name)
{
    // Check if name is in candidate, if so update vote
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcasecmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes++;
            return true;
        }
    }
        
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // sort candidates by candidate.votes to get the max value(s)
    int len_candidates = sizeof(candidates) / sizeof(candidates[0]);
    sort(candidates, len_candidates);
    
    // Get index of max value to access the candidate name
    int max = candidates[len_candidates - 1].votes;
    for (int i = 0; i < len_candidates; i++)
    {
        if (candidates[i].votes == max)
        {
            printf("%s\n", candidates[i].name);
        }
    }

}

// Sort array of candidates using selection sort algorithm 
void sort(candidate *array, int size) 
{
    for (int i = 0; i < size; i++)
    {
        for (int j = i + 1; j < size; j++)
        {
            if (array[i].votes > array[j].votes)
            {
                candidate temp;
                temp = array[i];
                array[i] = array[j];
                array[j] = temp;
            }
        }
    }
    
}
