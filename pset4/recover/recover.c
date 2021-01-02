#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h> 

typedef uint8_t BYTE;

// Function prototypes
FILE *create_jpeg_file(int count);
bool is_jpeg_header(BYTE *buffer);

int main(int argc, char *argv[])
{
    // Check for command line
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open image.raw for read
    FILE *file = fopen(argv[1], "r");

    // Check if file exists
    if (file == NULL)
    {
        printf("file does not exists");
        return 1;
    }

    // Empty output file to write recovered images
    FILE *output = NULL;
    BYTE *buffer = malloc(512);
    int counter = 0;

    while (fread(buffer, sizeof(buffer), 1, file))
    {
        // Check if signature
        if (is_jpeg_header(buffer))
        {
            // Close previous file if exists
            if (counter > 0)
            {
                fclose(output);
            }

            output = create_jpeg_file(counter);
            counter++;
        }

        // Skip first run since we have no data to write
        if (counter == 0) 
        {
            continue;
        }

        // Write the data to the file
        fwrite(buffer, sizeof(buffer), 1, output);
    }

    fclose(output);
    fclose(file);
    free(buffer);
    return 0;
}

// Checks if buffer represents a jpeg header
bool is_jpeg_header(BYTE *buffer)
{
    return (buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0);
}

// Generates new file
FILE *create_jpeg_file(int count)
{
    // Generate a new name and create new file
    char filename[32];
    sprintf(filename, "%03i.jpg", count);
    return fopen(filename, "w");
}