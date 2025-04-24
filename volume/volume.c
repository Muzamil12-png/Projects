#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open input file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open output file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // Copy the header from the input file to the output file
    uint8_t header[HEADER_SIZE];
    // reading the header from the input file provided
    if (fread(header, sizeof(uint8_t), HEADER_SIZE, input) != HEADER_SIZE)
    {
        fclose(input);
        fclose(output);
        printf("Error reading WAV header.\n");
        return 1;
    }
    // handling the error case
    if (fwrite(header, sizeof(uint8_t), HEADER_SIZE, output) != HEADER_SIZE)
    {
        fclose(input);
        fclose(output);
        printf("Error writing WAV header.\n");
        return 1;
    }

    // Process the audio samples
    int16_t sample;
    // reading the file till the end
    while (fread(&sample, sizeof(int16_t), 1, input) == 1)
    {
        // Scale the sample
        int16_t scaled_sample = (int16_t) (sample * factor);

        // Write the modified sample to the output file
        if (fwrite(&scaled_sample, sizeof(int16_t), 1, output) != 1)
        {
            fclose(input);
            fclose(output);
            printf("Error writing audio data.\n");
            return 1;
        }
    }

    // Close files
    fclose(input);
    fclose(output);

    return 0;
}
