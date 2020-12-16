#include <math.h>
#include "helpers.h"
#include <stdbool.h>
#include <math.h>
#include <string.h>

// Function prototype
int min(int, int);
void swap(BYTE *, BYTE *);
bool valid(int i, int j, int height, int width);
void set_average(int i, int j, int height, int width, RGBTRIPLE image[height][width], RGBTRIPLE unmodified_image[height][width]);


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.000);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            image[i][j].rgbtRed = min(sepiaRed, 255);
            image[i][j].rgbtGreen = min(sepiaGreen, 255);
            image[i][j].rgbtBlue = min(sepiaBlue, 255);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {   
        for (int j = 0, k = width - 1; k > j ; j++, k--)
        {
            // Use two pointers to swap 
            swap(&image[i][j].rgbtRed, &image[i][k].rgbtRed);
            swap(&image[i][j].rgbtGreen, &image[i][k].rgbtGreen);
            swap(&image[i][j].rgbtBlue, &image[i][k].rgbtBlue);
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of the original image to read unmodified pixel values
    RGBTRIPLE unmodified_image[height][width];
    memcpy(unmodified_image, image, sizeof(RGBTRIPLE) * height * width);
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Set the colors of the pixel (i, j) to the average of the surrounding pixels
            set_average(i, j, height, width, image, unmodified_image);
        }
    }
    return;
}

// Min return min of two integers
int min(int x, int y)
{
    if (x > y)
    {
        return y;
    }
    return x;
}

// Swap function
void swap(BYTE *x, BYTE *y)
{
    BYTE temp = *x;
    *x = *y;
    *y = temp;
}

// Function to determine valid index for blur box
bool valid(int i, int j, int height, int width)
{
    return (i >= 0 && i < height) && (j >= 0 && j < width);
}

// Function to set_average for new blur pixels
void set_average(int i, int j, int height, int width, RGBTRIPLE image[height][width], RGBTRIPLE unmodified_image[height][width])
{
    // blur box matrix 3x3 that stores indexes of neighbors pixels
    int box[3][3][2] = { 
        { {i - 1, j - 1}, {i - 1, j}, {i - 1, j + 1} }, 
        { {i    , j - 1}, {i    , j}, {i    , j + 1} }, 
        { {i + 1, j - 1}, {i + 1, j}, {i + 1, j + 1} }
    };
    
    int sumRed = 0, sumGreen = 0, sumBlue = 0;
    float counter = 0;
    
    // Loop over blur box of a given pixel (i, j) and get neighbors values if their index is valid
    for (int k = 0; k < 3; k++)
    {
        for (int p = 0; p < 3; p++)
        {
            // Get the indexes of each neighbor of (i, j) in the blur box 3x3 from the temp image
            int nx = box[k][p][0];
            int ny = box[k][p][1];
            
            if (valid(nx, ny, height, width))
            {
                sumRed += unmodified_image[nx][ny].rgbtRed;
                sumGreen += unmodified_image[nx][ny].rgbtGreen;
                sumBlue += unmodified_image[nx][ny].rgbtBlue;

                counter++;
            }
        }
    }
    
    // Set values of original image to new blurred values
    image[i][j].rgbtRed = round(sumRed / counter);
    image[i][j].rgbtGreen = round(sumGreen / counter);
    image[i][j].rgbtBlue = round(sumBlue / counter);
}
