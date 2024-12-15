#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1024
#define MAX_PATH_LENGTH 2048
#define MAX_PATHS 1000

// Struct to hold the path and its length
typedef struct {
    char path[MAX_PATH_LENGTH];
    int length;
} PathLength;

// Comparator function for sorting path lengths in descending order
int comparePathLength(const void *a, const void *b) {
    return ((PathLength *)b)->length - ((PathLength *)a)->length;
}

int main() {
    FILE *inputFile = fopen("input.txt", "r");
    if (inputFile == NULL) {
        perror("Error opening input file");
        return 1;
    }

    // Array to hold the paths and their lengths
    PathLength pathLengths[MAX_PATHS];
    int pathCount = 0;

    // Step 1: Mapper - Read paths from input file and calculate their lengths
    char line[MAX_LINE_LENGTH];
    while (fgets(line, sizeof(line), inputFile)) {
        line[strcspn(line, "\n")] = 0;  // Remove newline character

        // Store the path and its length
        if (pathCount < MAX_PATHS) {
            strcpy(pathLengths[pathCount].path, line);
            pathLengths[pathCount].length = strlen(line);
            pathCount++;
        } else {
            printf("Warning: Maximum number of paths exceeded. Some paths may be skipped.\n");
            break;
        }
    }
    fclose(inputFile);

    // Step 2: Sort the paths by length in descending order using qsort
    qsort(pathLengths, pathCount, sizeof(PathLength), comparePathLength);

    // Step 3: Reducer - Find and output the longest path(s)
    FILE *finalOutputFile = fopen("final_output.txt", "w");
    if (finalOutputFile == NULL) {
        perror("Error opening final output file");
        return 1;
    }

    if (pathCount > 0) {
        // The longest path length
        int maxLength = pathLengths[0].length;

        // Output all paths with the maximum length
        for (int i = 0; i < pathCount; i++) {
            if (pathLengths[i].length == maxLength) {
                fprintf(finalOutputFile, "%s\n", pathLengths[i].path);
            }
        }
    }

    fclose(finalOutputFile);

    return 0;
}
