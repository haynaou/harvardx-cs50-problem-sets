#include <stdio.h>
#include <cs50.h>
#include <math.h>


int main(void)
{
    float change;
    
    // Prompt till condition is met
    do
    {
        // Prompt the user to enter how much change is owed
        change = get_float("Change is owed? ");
    }
    while (change <= 0);
    
    // Convert from dollar to cent
    int cent = round(change * 100);
    
    // Initiate a coin counter
    int coins = 0;
    
    // Calculate the number of coin to return 
    do
    {
        if (cent >= 25)
        {
            cent = cent - 25;
            coins++;
        }
        
        else if (cent >= 10)
        {
            cent = cent - 10;
            coins++;
        }
        
        else if (cent >= 5)
        {
            cent = cent - 5;
            coins++;
        }
        
        else if (cent >= 1)
        {
            cent = cent - 1;
            coins++;
        }
        
    }
    
    while (cent != 0);
    
    
    // Print number of coins used
    printf("%i\n", coins);
}
