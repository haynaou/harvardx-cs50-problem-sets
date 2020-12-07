#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    
    // Prompt the user to enter the height of the pyramid 
    do
    {
        height = get_int("Positive number: ");
    }
    while ( (height <= 0) || (height > 8) );
 
    // Iterating over rows
    for (int row = 0; row < height ; row++)
    {
        // Printing spaces
        for (int i = 0; i < height - row - 1 ; i++)
        {
            printf(" ");

        }
        
        // Printing hashes
        for (int j = 0; j < row + 1 ; j++)
        {
            printf("#");

        }
        
        // Printing newline
        printf("\n");
    }
    
    
}
