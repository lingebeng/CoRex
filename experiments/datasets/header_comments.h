/*
 * C/C++ Header File Comment Examples
 * Header files have special comment patterns for documentation
 */

#ifndef HEADER_COMMENTS_H
#define HEADER_COMMENTS_H

// Include guard comments
// Prevents multiple inclusion of the same header

/**
 * @file header_comments.h
 * @brief Header file demonstrating various comment styles
 * @author Example Author
 * @version 1.0
 * @date 2025-10-31
 *
 * Detailed file description goes here.
 */

#ifdef __cplusplus
extern "C" {  // C++ compatibility
#endif

/*
 * Macro definitions with documentation
 */

/**
 * @def MAX_SIZE
 * @brief Maximum buffer size
 */
#define MAX_SIZE 1024

/// Minimum value constant
#define MIN_VALUE 0

/*
 * Type definitions
 */

/**
 * @typedef ErrorCode
 * @brief Error code enumeration type
 */
typedef enum {
    ERROR_NONE = 0,      ///< No error
    ERROR_INVALID = -1,  ///< Invalid parameter
    ERROR_MEMORY = -2,   ///< Memory allocation failed
    ERROR_IO = -3        ///< I/O error
} ErrorCode;

/**
 * @struct Point
 * @brief Represents a 2D point
 *
 * This structure stores x and y coordinates.
 */
typedef struct Point {
    int x;  ///< X coordinate
    int y;  ///< Y coordinate
} Point;

/**
 * @struct Configuration
 * @brief Configuration settings structure
 */
typedef struct {
    int timeout;          ///< Timeout in seconds
    char *hostname;       ///< Server hostname
    unsigned int port;    ///< Server port number
    int verbose;          ///< Verbose output flag
} Configuration;

/*
 * Function declarations
 */

/**
 * @brief Initialize the system
 * @param config Configuration settings
 * @return Error code (ERROR_NONE on success)
 *
 * This function must be called before any other functions.
 * It initializes internal data structures and resources.
 *
 * @note Thread-safe
 * @warning Must be called only once
 */
ErrorCode initialize(Configuration *config);

/**
 * @brief Process data buffer
 * @param[in] input Input buffer
 * @param[in] input_size Size of input buffer
 * @param[out] output Output buffer
 * @param[in,out] output_size Input: size of output buffer, Output: bytes written
 * @return Error code
 *
 * @pre input must not be NULL
 * @pre input_size must be > 0
 * @post output contains processed data
 *
 * @see cleanup()
 */
ErrorCode process(const char *input, size_t input_size,
                  char *output, size_t *output_size);

/**
 * @brief Cleanup and release resources
 *
 * Call this function when done to free all allocated resources.
 *
 * @note Not thread-safe
 */
void cleanup(void);

// Inline function documentation
/**
 * @brief Check if value is valid
 * @param value Value to check
 * @return 1 if valid, 0 otherwise
 */
static inline int is_valid(int value) {
    return value >= MIN_VALUE && value <= MAX_SIZE;
}

#ifdef __cplusplus
}  // extern "C"
#endif

/*
 * C++ specific section
 */
#ifdef __cplusplus

/**
 * @namespace utils
 * @brief Utility functions namespace
 */
namespace utils {

/**
 * @class Logger
 * @brief Logging utility class
 *
 * Provides thread-safe logging capabilities.
 */
class Logger {
public:
    /**
     * @brief Log levels
     */
    enum Level {
        DEBUG,   ///< Debug messages
        INFO,    ///< Informational messages
        WARNING, ///< Warning messages
        ERROR    ///< Error messages
    };

    /**
     * @brief Get logger instance (singleton)
     * @return Reference to logger instance
     */
    static Logger& getInstance();

    /**
     * @brief Log a message
     * @param level Log level
     * @param message Message to log
     */
    void log(Level level, const char *message);

    // Deleted copy constructor (C++11)
    Logger(const Logger&) = delete;  ///< Non-copyable

    // Deleted assignment operator (C++11)
    Logger& operator=(const Logger&) = delete;  ///< Non-assignable

private:
    /**
     * @brief Private constructor for singleton
     */
    Logger();

    /**
     * @brief Destructor
     */
    ~Logger();
};

/**
 * @brief Template function example
 * @tparam T Type parameter
 * @param value Input value
 * @return Maximum of value and zero
 */
template<typename T>
T max_with_zero(T value) {
    return value > static_cast<T>(0) ? value : static_cast<T>(0);
}

}  // namespace utils

#endif  // __cplusplus

// Conditional compilation comments
#ifdef DEBUG
/**
 * @brief Debug-only function
 * @param msg Debug message
 *
 * Only available in debug builds
 */
void debug_print(const char *msg);
#endif

// Platform-specific comments
#ifdef _WIN32
// Windows-specific declarations
#elif defined(__linux__)
// Linux-specific declarations
#elif defined(__APPLE__)
// macOS/iOS-specific declarations
#endif

// TODO: Add more utility functions
// FIXME: Thread safety needs review
// NOTE: API is subject to change
// DEPRECATED: Use new_function() instead

/**
 * @deprecated Use process() instead
 * @brief Old function (deprecated)
 */
ErrorCode old_function(void);

/*
 * End of header file
 */

#endif  // HEADER_COMMENTS_H

// vim: set ts=4 sw=4 et:
// Editor configuration comments
