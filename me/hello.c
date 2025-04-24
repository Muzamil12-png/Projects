// Added libraries of codes
#include <cs50.h>
#include <stdio.h>
// Ask the user about their name and once they input their name reply with hello user input
int main(void)
{
    string answer = get_string("What's your name? ");
    printf("hello, %s\n", answer);
}
