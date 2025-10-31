/*
 * This is a multi-line comment (C-style)
 * Often used for file headers and large comment blocks
 * Can span multiple lines
 */

// Single-line comment (C++-style)
// This is the most common type in modern C++

/**
 * @file cpp_comments.cpp
 * @brief Doxygen-style documentation comment
 * @author Example Author
 * @date 2025-10-31
 *
 * This file demonstrates various comment types in C/C++
 */

#include <iostream>

// ==========================================
// Section divider using single-line comments
// ==========================================

/*******************************************
 * Box-style multi-line comment
 *******************************************/

/**
 * @brief Function with Doxygen documentation
 * @param x First parameter
 * @param y Second parameter
 * @return Sum of x and y
 */
int add(int x, int y) {
    return x + y;  // End-of-line comment
}

/// Qt-style documentation comment (single-line)
/// This style is used in Qt and other frameworks
/// Can span multiple lines with /// on each line
int multiply(int a, int b) {
    return a * b;
}

//! Another Qt-style documentation comment
//! Using exclamation mark instead of third slash
int subtract(int a, int b) {
    return a - b;
}

/*!
 * Qt-style multi-line documentation
 * Uses exclamation mark inside the comment
 * \param a First parameter
 * \param b Second parameter
 * \return The division result
 */
double divide(double a, double b) {
    return a / b;
}

/**
 * @class SampleClass
 * @brief Example class with Doxygen comments
 *
 * Detailed description of the class.
 */
class SampleClass {
public:
    /**
     * @brief Constructor
     */
    SampleClass() : value(0) {}

    /**
     * @brief Get the value
     * @return Current value
     */
    int getValue() const { return value; }

    /// Set the value (Qt-style brief comment)
    void setValue(int v) { value = v; }

private:
    int value;  ///< Member variable comment (Doxygen style)
};

/* Nested comments are NOT allowed in C/C++:
 * /* This would cause an error */
 * But this line is fine
 */

// TODO: This is a TODO comment
// FIXME: This needs to be fixed
// NOTE: Important note here
// XXX: Warning or attention needed
// HACK: Temporary workaround
// BUG: Known bug

#if 0
/*
 * Multi-line comment using preprocessor
 * This is a common trick to comment out large blocks
 * including other comments
 */
int disabled_function() {
    // This code won't be compiled
    return 42;
}
#endif

int main() {
    /* Traditional C-style comment */
    int x = 10;

    // Modern C++ style comment
    int y = 20;

    int z = x + y;  /* Inline C-style comment */

    /*
     * Multi-line comment
     * with nice formatting
     * using asterisks
     */

    // Multiple single-line comments
    // used to create a block
    // of commented text

    return 0;
}

// Special characters in comments: é, ñ, 中文, 日本語, 한글
// Comment with code snippet: std::cout << "Hello" << std::endl;
// Comment with URL: https://example.com
// Comment with path: /usr/local/include/header.h
