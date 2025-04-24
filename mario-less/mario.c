#include <stdio.h>

int main()
{
    int i, j, height = 0;

    while (height <= 0)
    {
        printf("Height: ");
        scanf("%d", &height);
    }

    for (i = 0; i < height; i++)
    {
        for (j = 0; j < height - i - 1; j++)
        {
            printf(" ");
        }
        for (j = 0; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }

    return 0;
}
