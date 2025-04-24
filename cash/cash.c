#include <cs50.h>
#include <stdio.h>

int main()
{
    int value = -1, quotient, remainder;
    int coins = 0;

    while (value < 0)
    {
        printf("Change owed:");
        scanf("%d", &value);
    }

    if (value >= 25)
    {
        quotient = value / 25;
        remainder = value % 25;
        coins = coins + quotient;
        value = remainder;
    }

    if (value >= 10)
    {
        quotient = value / 10;
        remainder = value % 10;
        coins = coins + quotient;
        value = remainder;
    }

    if (value >= 5)
    {
        quotient = value / 5;
        remainder = value % 5;
        coins = coins + quotient;
        value = remainder;
    }

    if (value >= 1)
    {
        coins = coins + value;
    }

    printf("%d", coins);

    return 0;
    printf("\n");
}
