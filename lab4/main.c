#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1024
#define MAX_WORD_LENGTH 100

// Struct to hold word and its count
typedef struct {
    char word[MAX_WORD_LENGTH];
    int count;
} WordCount;

// Function to process the mapper
void mapper(FILE *inputFile, WordCount *wordCounts, int *wordCountSize) {
    char line[MAX_LINE_LENGTH];
    while (fgets(line, sizeof(line), inputFile)) {
        // Split the line into words
        char *word = strtok(line, " \n");
        while (word != NULL) {
            int found = 0;
            // Check if the word already exists in the array
            for (int i = 0; i < *wordCountSize; i++) {
                if (strcmp(wordCounts[i].word, word) == 0) {
                    wordCounts[i].count++;  // Increment the count for the existing word
                    found = 1;
                    break;
                }
            }
            // If the word is not found, add it to the array
            if (!found) {
                strcpy(wordCounts[*wordCountSize].word, word);
                wordCounts[*wordCountSize].count = 1;
                (*wordCountSize)++;
            }
            word = strtok(NULL, " \n");
        }
    }
}

// Comparison function for sorting the words
int compareWordCount(const void *a, const void *b) {
    return strcmp(((WordCount *)a)->word, ((WordCount *)b)->word);
}

// Function to process the reducer and write the final output
void reducer(WordCount *wordCounts, int wordCountSize, FILE *outputFile) {
    for (int i = 0; i < wordCountSize; i++) {
        fprintf(outputFile, "%s\t%d\n", wordCounts[i].word, wordCounts[i].count);
    }
}

int main() {
    FILE *inputFile = fopen("input.txt", "r");
    if (inputFile == NULL) {
        perror("Error opening input file");
        return 1;
    }

    // Array to hold words and their counts
    WordCount wordCounts[MAX_LINE_LENGTH];
    int wordCountSize = 0;

    mapper(inputFile, wordCounts, &wordCountSize);
    fclose(inputFile);

    qsort(wordCounts, wordCountSize, sizeof(WordCount), compareWordCount);

    FILE *finalOutputFile = fopen("final_output.txt", "w");
    if (finalOutputFile == NULL) {
        perror("Error opening final output file");
        return 1;
    }

    reducer(wordCounts, wordCountSize, finalOutputFile);
    fclose(finalOutputFile);
    return 0;
}
