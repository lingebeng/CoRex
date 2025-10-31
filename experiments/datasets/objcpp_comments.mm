/*
 * Objective-C++ Comment Examples (.mm file)
 * Combines Objective-C and C++ syntax
 * Uses the same comment styles as C/C++/Objective-C
 */

#import <Foundation/Foundation.h>
#include <iostream>
#include <vector>

// Single-line comment (C++/Objective-C style)
// This works in both Objective-C and C++ parts

/**
 * @brief Objective-C interface declaration
 * @discussion This class demonstrates Objective-C comments
 *
 * Detailed description of the class can go here.
 * Can include examples, usage notes, etc.
 */
@interface SampleClass : NSObject

/**
 * @brief Instance variable with documentation
 */
@property (nonatomic, strong) NSString *name;  ///< Doxygen-style inline comment

/**
 * @brief Instance method
 * @param value The input value to process
 * @return Processed string result
 *
 * @discussion This method demonstrates Objective-C method comments
 */
- (NSString *)processValue:(NSInteger)value;

/**
 * @brief Class method
 * @return A new instance of SampleClass
 */
+ (instancetype)sharedInstance;

@end

/**
 * Implementation section
 */
@implementation SampleClass

/// Qt-style documentation comment
/// Initializes a new instance
- (instancetype)init {
    self = [super init];
    if (self) {
        // Initialize properties
        _name = @"Default";  // Inline comment
    }
    return self;
}

/*
 * Multi-line comment in implementation
 * Can span multiple lines
 */
- (NSString *)processValue:(NSInteger)value {
    // Convert integer to string
    return [NSString stringWithFormat:@"Value: %ld", (long)value];
}

+ (instancetype)sharedInstance {
    static SampleClass *instance = nil;
    static dispatch_once_t onceToken;

    /*
     * Thread-safe singleton pattern
     * Using GCD dispatch_once
     */
    dispatch_once(&onceToken, ^{
        instance = [[self alloc] init];
    });

    return instance;
}

@end

// ========================================
// C++ Section
// ========================================

/**
 * @brief C++ class in Objective-C++ file
 * @tparam T Template parameter type
 *
 * This demonstrates mixing C++ and Objective-C
 */
template<typename T>
class CppClass {
public:
    /**
     * @brief Constructor
     * @param value Initial value
     */
    CppClass(T value) : data(value) {}

    /**
     * @brief Get the stored value
     * @return Reference to the data
     */
    T& getValue() { return data; }

    /// Set the value (Qt-style)
    void setValue(T value) { data = value; }

private:
    T data;  ///< Stored data member
};

/*
 * Function mixing Objective-C and C++
 */
void mixedFunction() {
    // C++ STL usage
    std::vector<int> numbers = {1, 2, 3, 4, 5};

    // Objective-C object
    NSMutableArray *array = [NSMutableArray array];

    /*
     * Convert C++ vector to NSArray
     * Demonstrates Objective-C++ bridge
     */
    for (int num : numbers) {
        [array addObject:@(num)];  // Box primitive in NSNumber
    }

    // C++ iostream
    std::cout << "Array count: " << [array count] << std::endl;
}

#pragma mark - Section Markers

/*
 * #pragma mark is Objective-C specific
 * Used for organizing code in Xcode
 */

#pragma mark - Helper Functions

/**
 * @brief Helper function with C++ and Objective-C
 * @param objcString Objective-C NSString
 * @return C++ std::string
 */
std::string convertNSStringToStdString(NSString *objcString) {
    // Convert NSString to C++ string
    return std::string([objcString UTF8String]);
}

/**
 * @brief Convert C++ string to NSString
 * @param cppString C++ std::string
 * @return Objective-C NSString
 */
NSString* convertStdStringToNSString(const std::string& cppString) {
    return [NSString stringWithUTF8String:cppString.c_str()];
}

#pragma mark - Block Comments

// Blocks are Objective-C closures
typedef void(^CompletionBlock)(BOOL success, NSError *error);

/**
 * @brief Function using blocks
 * @param completion Completion handler block
 *
 * Blocks are documented like other parameters
 */
void performAsyncOperation(CompletionBlock completion) {
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
        // Simulate async work
        sleep(1);

        // Call completion on main thread
        dispatch_async(dispatch_get_main_queue(), ^{
            if (completion) {
                completion(YES, nil);
            }
        });
    });
}

// TODO: Add error handling
// FIXME: Memory leak in convertNSStringToStdString
// NOTE: Requires ARC (Automatic Reference Counting)
// XXX: Deprecated in iOS 15+
// WARNING: This method is not thread-safe

#if 0
/*
 * Disabled code using preprocessor
 * Works the same in Objective-C++ as in C++
 */
- (void)deprecatedMethod {
    // Old implementation
}
#endif

/*****************************************************
 * Objective-C Specific Comment Patterns
 *****************************************************/

// @interface - Class interface declaration
// @implementation - Class implementation
// @property - Property declaration
// @synthesize - Property synthesizer (legacy)
// @protocol - Protocol declaration
// @selector - Method selector
// #pragma mark - Code organization marker

/**
 * Protocol with documentation
 */
@protocol SampleProtocol <NSObject>

/**
 * @brief Required method
 * @param data Data to process
 */
- (void)processData:(NSData *)data;

@optional
/**
 * @brief Optional method
 * @return Success status
 */
- (BOOL)validate;

@end

// Special characters: 中文注释, 日本語コメント, 한글 주석, العربية
// Comment with selector: @selector(processValue:)
// Comment with protocol: id<SampleProtocol>
