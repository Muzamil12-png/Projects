#include <ctype.h>
#include <math.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Global variable to track word count
unsigned int count_words = 0;

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

const unsigned int N = 20000; // Number of buckets in hash table

// Hash table array
node *table[N];

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int roll_sum = 0;
    unsigned int squared = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        squared = pow(toupper(word[i]), 2); // Square the character value
        if (i == round(strlen(word) / 2))
        {
            roll_sum = roll_sum + round(sqrt(roll_sum)) + 17; // Some random manipulations
        }
        roll_sum = squared + roll_sum + 47; // Additional random factor
    }
    return roll_sum % N; // Return hash index
}

// Checks if word is in the dictionary
bool check(const char *word)
{
    int word_index = hash(word);      // Get hash index for the word
    node *cursor = table[word_index]; // Get cursor to the list at that index

    // Traverse the linked list
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0) // Compare ignoring case
        {
            return true; // Word found
        }
        cursor = cursor->next; // Move to the next node in the list
    }
    return false; // Word not found
}

// Loads dictionary into memory, returning true if successful, false if error occurs
bool load(const char *dictionary)
{
    FILE *dict_open = fopen(dictionary, "r"); // Open dictionary file
    if (dict_open == NULL)
    {
        printf("Could not open the dictionary file.\n");
        return false; // Return false if file opening fails
    }

    char buffer[LENGTH + 1]; // Buffer to hold each word
    while (fscanf(dict_open, "%s", buffer) != EOF)
    {
        node *n = malloc(sizeof(node)); // Allocate memory for a new node
        if (n == NULL)
        {
            fclose(dict_open); // Close the file before returning
            return false;      // Return false if memory allocation fails
        }

        strcpy(n->word, buffer); // Copy word into new node
        n->next = NULL;          // Set next pointer to NULL initially

        int hash_index = hash(buffer); // Get hash index for the word

        // Insert node into hash table (linked list at the index)
        if (table[hash_index] == NULL)
        {
            table[hash_index] = n; // If no node exists, place the new node at the index
        }
        else
        {
            n->next = table[hash_index]; // Add new node to the front of the list
            table[hash_index] = n;
        }

        count_words++; // Increment word count
    }

    fclose(dict_open); // Close the dictionary file after reading all words
    return true;
}

// Returns the number of words in the dictionary, or 0 if not loaded
unsigned int size(void)
{
    return count_words;
}

// Unloads dictionary from memory, returning true if successful
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i]; // Get the list at the index

        // Traverse the linked list
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next; // Move to the next node
            free(temp);            // Free the memory for the current node
        }
    }
    return true; // Return true if successful
}
