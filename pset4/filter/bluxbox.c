#include <stdio.h>

int main(void)
{
    int i = 1, j = 1;
    
    int box[3][3][2] = { { {i - 1, j - 1}, {i - 1, j}, {i - 1, j + 1} }, { {i, j - 1}, {i, j}, {i, j + 1} }, { { i + 1, j - 1}, {i + 1, j }, {i + 1, j + 1} }};
    
    for (int k = 0; k < 3; k++)
    {
        for (int p = 0; p < 3; p++)
        {
            printf("[%d, %d] ", box[k][p][0], box[k][p][1]);
        }
        
        printf("\n");
    };
}