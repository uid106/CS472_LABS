// This is a short brainf[ric]k interpreter without input ("," operator)
// it can be tested here: https://code.golf/brainfuck#cpp
#include <cstdio>

// Brainfuck is a minimal programing langauge with 8 operators. It
// operates on an array of memory cells, each initially set to zero,
// with a memory pointer that can move left (<) or right (>). You can
// increment (+) or decrement (-) the current memory cell. You can
// also output the current memory cell as a character (., and control
// loops using [ and ] based on the value at the memory pointer.

// example hello world program from https://en.wikipedia.org/wiki/Brainfuck:
// ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.

// Programs are given as command line arguments. Multiple programs can be given
int main(int argc, char** argv) {
    // Loop through all provided programs
    for (int fileIndex = 1; fileIndex < argc; ++fileIndex) {
        // Initialize memory and instruction pointers
        int memory[2048] = {0};   // Memory tape of size 2048
        int memoryPointer = 0;   // Points to the current memory cell
        int instructionPointer = 0;  // Points to the current instruction in the source code
        int loopCounter, direction;  // Loop handling variables

        // While there are more instructions to process in the current argument
        while (argv[fileIndex][instructionPointer] != '\0') {
            // Fetch the current instruction
            char instruction = argv[fileIndex][instructionPointer];

            // Brainfuck commands implementation
            switch (instruction) {
                case '>': 
                    // Move the memory pointer to the right
                    ++memoryPointer;
                    break;
                case '<': 
                    // Move the memory pointer to the left
                    --memoryPointer;
                    break;
                case '+': 
                    // Increment the value at the memory pointer
                    ++memory[memoryPointer];
                    break;
                case '-': 
                    // Decrement the value at the memory pointer
                    --memory[memoryPointer];
                    break;
                case '.': 
                    // Output the value at the memory pointer as a character
                    putchar(memory[memoryPointer]);
                    break;
                case '[': 
                    // If the value at the memory pointer is zero, jump to the matching ']'
                    if (memory[memoryPointer] == 0) {
                        loopCounter = 1; // keeps track of matching parenthesis
                        while (loopCounter != 0) { // stop when all brackets have been closed. 
                            ++instructionPointer;
                            if (argv[fileIndex][instructionPointer] == '[') ++loopCounter;
                            if (argv[fileIndex][instructionPointer] == ']') --loopCounter;
                        }
                    }
                    break;
                case ']': 
                    // If the value at the memory pointer is non-zero, jump back to the matching '['
                    if (memory[memoryPointer] != 0) {
                        loopCounter = 1;
                        while (loopCounter != 0) {
                            --instructionPointer;
                            if (argv[fileIndex][instructionPointer] == '[') --loopCounter;
                            if (argv[fileIndex][instructionPointer] == ']') ++loopCounter;
                        }
                    }
                    break;
            }
            // Move to the next instruction
            ++instructionPointer;
        }
    }
}
