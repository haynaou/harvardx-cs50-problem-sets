#include <stdio.h>
#include <cs50.h>

int main(void)
// funtion to get the user input to say hello username
{
    string name = get_string("What's your name?\n");
    printf("hello, %s\n", name);
}
