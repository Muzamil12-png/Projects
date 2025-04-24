#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// defining the size of the block to read from the image
#define BLOCK_SIZE 512

// JPEG signature for identifying the image start
const uint8_t JPEG_HEADER[] = {0xFF, 0xD8, 0xFF};

// making suer that the image starts with JPEG signature
int is_jpeg_start(uint8_t *block)
{
    // Check the first three bytes for 0xFF, 0xD8, 0xFF
    if (block[0] == JPEG_HEADER[0] && block[1] == JPEG_HEADER[1] && block[2] == JPEG_HEADER[2])
    {
        // Check the fourth byte (should be 0xE0 to 0xEF)
        if (block[3] >= 0xE0 && block[3] <= 0xEF)
        {
            return 1;
        }
    }
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Opening the image file
    FILE *input_file = fopen(argv[1], "rb");
    if (input_file == NULL)
    {
        printf("Could not open file %s.\n", argv[1]);
        return 1;
    }

    // a buffer that will hold 512-byte blocks
    uint8_t buffer[BLOCK_SIZE];
    FILE *output_file = NULL;
    int file_count = 0;
    char filename[8];

    while (fread(buffer, 1, BLOCK_SIZE, input_file) == BLOCK_SIZE)
    {
        if (is_jpeg_start(buffer))
        {
            if (output_file != NULL)
            {
                fclose(output_file);
                output_file = NULL;
            }

            // Creating a new fil ename for the next JPEG
            sprintf(filename, "%03d.jpg", file_count++);
            output_file = fopen(filename, "wb");
            if (output_file == NULL)
            {
                printf("Could not create file %s.\n", filename);
                fclose(input_file);
                return 1;
            }
        }

        // writing to the next block
        if (output_file != NULL)
        {
            fwrite(buffer, 1, BLOCK_SIZE, output_file);

            if (buffer[BLOCK_SIZE - 2] == 0xFF && buffer[BLOCK_SIZE - 1] == 0xD9)
            {
                fclose(output_file);
                output_file = NULL; // Reseting to ensure new JPEGs are detected
            }
        }
    }

    if (output_file != NULL)
    {
        fclose(output_file);
    }

    fclose(input_file);

    printf("Recovered %d JPEG(s).\n", file_count);
    return 0;
}
