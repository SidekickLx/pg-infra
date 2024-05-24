

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
    Your task is to generate a code snippet that fix the vulerability. Do not output other irrelavent information!
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