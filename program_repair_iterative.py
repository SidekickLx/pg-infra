import os, sys, random
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM
from langchain.chains import LLMChain 
from goalkeeper_test_patch import test_patch
from utils import *

def goal_keeper(repaired_code, tgt_proj="linux"):
    # TODO: generate patch
    
    feedback = test_patch(patch, tgt_proj)
    '''
    {
    'build_status': build_status,
    'build_output': build_output,
    'pov_results': pov_results,
    'test_status': test_status,
    'test_output': test_output
    }
    '''
    # TODO: wrapper

    return feedback


if __name__ == "__main__":

    litellm = ChatLiteLLM(model="gpt-3.5-turbo") # use LiteLLM Interface
    execute_task_prompt = PromptTemplate(
        template= """You are a cybersecurity expert that is responsible to repair a vulnerable code.
        {code}
        Your task is to generate a code snippet that fix the vulerability. Do not output other irrelavent information!
        Here are some useful information that can help you identify the vulerability. There will be an 'N/A' if the information is not availiable.
        Possible line number of the vulerability: {line_number}
        The type of the Vulnerability : {vul_type}
        You will also be provided with sample repairs from the previous iteration and the feedback from an auto-test program.
        sample repair: {reapired_code}
        feedback: {harness_fdbk}
        Begin!
        """,
        input_variables=["code", "pr_tools", "line_number", "vul_type", "reapired_code", "harness_fdbk" ],
    )


    input_json = {}
    llm_chain = LLMChain(llm=litellm, prompt=execute_task_prompt)
    # A code sample from openssl)
    code = load_code_need_to_fix(input_json)
    line_number = 'N/A' # TODO: collect line number info from static analysis
    reapired_code = "N/A"
    harness_fdbk = "N/A"


    while True:
        # the main loop for iterative program repair
        repaired_code = llm_chain.invoke(
            {
                "code": code,
                "line_number": line_number  ,
                "vul_type": "N/A",
                "reapired_code": reapired_code,
                "harness_fdbk": harness_fdbk,
            },return_only_outputs=True
            )
        feed_back = goal_keeper(repaired_code)
        if feed_back['build_status'] == 'pass' and feed_back['test_status'] == 'pass':
            break
        elif feed_back['build_status'] == 'pass' and feed_back['test_status'] == 'fail':
            # TODO: process pov_results and add it to the prompt
            harness_fdbk = feed_back['test_output']
            continue
        elif feed_back['build_status'] == 'fail':
            harness_fdbk = feed_back['build_output']
            continue
