

# Prompt for iterative auto program repair.
ITERATIVE_PROMPTS = \
"""
    You are a cybersecurity expert. Here is a function that contains a vulerability.
    {code}
    Fix the vulerability in the code and output the complete fixed function. Do not output other irrelavent information!
    Here are some useful information that can help you identify the vulerability. There will be an 'N/A' if the information is not availiable.
    Possible line number of the vulerability: {line_number}
    The type of the Vulnerability : {vul_type}
    You will also be provided with sample repairs from the previous iteration and the feedback from an auto-test program.
    sample repair: {reapired_code}
    feedback: {harness_fdbk}
    Begin!
"""

# Prompt prefix for the agent 
AGENT_PROMPT_PREFIX = \
"""
    You are a cybersecurity expert that is responsible to repair a vulnerable code.
    {code}
    Your task is to generate a code snippet that fix the vulerability. And test the patch with an goalkeeper program.
    You can use following tools {pr_tools}
    Here are some useful information that can help you identify the vulerability. There will be an 'N/A' if the information is not availiable.
    Possible line number of the vulerability: {line_number}
    The type of the Vulnerability : {vul_type}
    You will also be provided with sample repairs from the previous iteration and the feedback from an auto-test program.
    sample repair: {reapired_code}
    feedback: {harness_fdbk}
"""

# Prompt suffix for the agent
AGENT_PROMPT_SUFFIX = \
"""
    Begin! Remember to answer very politely.
    Previous conversation history:
    {chat_history}
    {agent_scratchpad}
"""

# general COT prefix:

COT_PREFIX = \
"""
Can you fix this code snippet? The code contains a vulnerability that needs to be fixed. And here is the description of the vulnerability:
"""


# COT for UAF

UAF_DESCRIPTION = \
"""
This code contains Use-After-Free vulnerability. Reffering to CWE-416. The use of previously-freed memory can have any number of adverse consequences, ranging from the corruption of valid data to the execution of arbitrary code, depending on the instantiation and timing of the flaw. The simplest way data corruption may occur involves the system's reuse of the freed memory. Use-after-free errors have two common and sometimes overlapping causes:

Error conditions and other exceptional circumstances.
Confusion over which part of the program is responsible for freeing the memory.
In this scenario, the memory in question is allocated to another pointer validly at some point after it has been freed. The original pointer to the freed memory is used again and points to somewhere within the new allocation. As the data is changed, it corrupts the validly used memory; this induces undefined behavior in the process.

If the newly allocated data happens to hold a class, in C++ for example, various function pointers may be scattered within the heap data. If one of these function pointers is overwritten with an address to valid shellcode, execution of arbitrary code can be achieved.
Here are demonstrative examples of UAF:

Example 1

(bad code)
Example Language: C 
char* ptr = (char*)malloc (SIZE);
if (err) {
abrt = 1;
free(ptr);
}
...
if (abrt) {
logError("operation aborted before commit", ptr);
}

The code snippet provided has a potential issue with using a freed pointer (ptr) in the logError function. When free(ptr) is called, the memory allocated to ptr is deallocated, making ptr a dangling pointer. Using this dangling pointer later, as in the call to logError, results in undefined behavior.

To fix this issue, we can ensure that the pointer is not used after it has been freed. 
1. Check malloc Return Value: Added a check to ensure malloc did not return nullptr, which would indicate allocation failure.
2. Setting Pointer to nullptr After Freeing: After calling free(ptr), ptr is set to nullptr to indicate that the memory has been freed and to avoid using a dangling pointer.
3. Handling Logging Gracefully: The logError function is called with ptr, which will be nullptr if the memory was freed. This prevents undefined behavior by avoiding the use of a dangling pointer.

Example 2

#include <iostream>
#include <crow.h>
(bad code)
Example Language: C++
int main() {
    crow::SimpleApp app;
    int* order_price = nullptr; // Create the pointer

    CROW_ROUTE(app, "/order/start")
    ([&order_price]() -> std::string {
        order_price = new int(25); // Allocate memory and assign the location to the pointer
        return "Order started for $" + std::to_string(*order_price);
    });

    CROW_ROUTE(app, "/order/confirm")
    ([&order_price]() -> std::string {
        // proccess_ticket(order_price)

        return "The price $" + std::to_string(*order_price) + " was noted on your ticket and will be charged upon entry";  // View the memory data at the pointer address
    });

    CROW_ROUTE(app, "/order/cancel")
    ([&order_price]() -> std::string {
        delete order_price; // Release the memory
        return "Order canceled";
    });

    app.port(8888).run();
}

The use-after-free vulnerability happens because the order_price pointer is deleted when the /order/cancel route is called, but the pointer is not set to nullptr. If a client tries to confirm an order after it has been canceled, the program will dereference a dangling pointer, leading to undefined behavior.
To fix this issue, we can ensure that the pointer is not used after it has been freed. 
1. After deleting order_price in the /order/cancel route, the pointer is set to nullptr to ensure it does not point to a freed memory location.
2. The /order/confirm route checks if order_price is nullptr before trying to use it, providing a proper message if no active order exists.

"""


# COT for OOB

OOB_DESCRIPTION = \
"""
An "Out of Bounds" vulnerability, often referred to as an "Out of Bounds Access" vulnerability, occurs when a program reads from or writes to memory locations that are outside the bounds of allocated memory buffers. 
These vulnerabilities can lead to various security issues, including data corruption, program crashes, and arbitrary code execution.

Here are demonstrative examples of OOB:


"""




