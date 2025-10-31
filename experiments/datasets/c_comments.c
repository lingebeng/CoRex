/*
 * C Language Comment Examples
 * Pure C only supports C-style comments (/* */)
 * C99 and later also support // comments
 */

#include <stdio.h>

/* Simple multi-line comment */

/*
 * Formatted multi-line comment
 * with leading asterisks
 * for better readability
 */

/**
 * Function documentation comment
 * Parameters:
 *   x - first integer
 *   y - second integer
 * Returns:
 *   sum of x and y
 */
int add(int x, int y) {
    return x + y;
}

// C99-style single-line comment
// Available in C99 standard and later

int multiply(int a, int b) {
    return a * b; /* inline comment */
}

/*
 * Function: divide
 * ----------------
 * Divides two numbers
 *
 * a: dividend
 * b: divisor
 *
 * returns: quotient
 */
double divide(double a, double b) {
    return a / b;
}

/**************************************************
 * Section header comment
 * Used to separate major sections of code
 **************************************************/

/* TODO: Implement error handling */
/* FIXME: This function has a memory leak */
/* NOTE: This assumes b is never zero */
/* XXX: Deprecated - use new_function instead */

typedef struct {
    int x;      /* x coordinate */
    int y;      /* y coordinate */
    int z;      /* z coordinate */
} Point3D;

/*
 * Structure: Point3D
 * ------------------
 * Represents a point in 3D space
 *
 * Members:
 *   x: x-axis coordinate
 *   y: y-axis coordinate
 *   z: z-axis coordinate
 */

int main() {
    /* Variable declarations with comments */
    int a = 10;  /* first number */
    int b = 20;  /* second number */

    // C99 style comments
    // Can be used in modern C code
    int result = a + b;

    /*
     * Long explanation that spans
     * multiple lines and provides
     * detailed information about
     * the following code block
     */

    printf("Result: %d\n", result);

    return 0;
}

/* End of file comment */
