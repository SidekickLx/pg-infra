import os, sys, random
import structures 
import prompts
import utils
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains.llm import LLMChain 


if __name__ == "__main__":

    input_json = utils.get_input_json()
    patch_name = "new_patch.diff"
    utils.download_project(input_json["project_name"])
    proj_obj = structures.Project(input_json)
    print(" Project downloaded successfully!")

    # from langchain_openai import ChatOpenAI
    # litellm = ChatOpenAI(model_name="gpt-4-turbo", streaming=True,  temperature=0) # use LiteLLM Interface
    litellm = ChatOpenAI(model="gemini-1.5-pro-preview-0409", 
                          temperature=0, 
                          max_tokens=8192,
                          api_key="sk-fnBdBgugSvfZ2ejzX6HFFQ",
                          base_url="https://aixcc.lyric.today:465", # specify the deployed url
                          ) # use LiteLLM Interface
    execute_task_prompt = PromptTemplate(
        template= prompts.ITERATIVE_PROMPTS,
        input_variables=["code", "line_number", "vul_type", "reapired_code", "harness_fdbk" ],
    )


    llm_chain = LLMChain(llm=litellm, prompt=execute_task_prompt)
    # A code sample from openssl
    code = proj_obj.code
    line_number = 'N/A' # TODO: collect line number info from static analysis
    reapired_code = "N/A"
    harness_fdbk = "N/A"

    iter = 0
    while True:
        print("iters: ", iter)
        # the main loop for iterative program repair
        try:            
            repaired_code = llm_chain.invoke(
                {
                    "code": code,
                    "line_number": line_number,
                    "vul_type": "N/A",
                    "reapired_code": reapired_code,
                    "harness_fdbk": harness_fdbk,
                },
                return_only_outputs=True
                )
        except Exception as e:
            print(e)
            break
        patch = utils.gen_patch(proj_obj, repaired_code, patch_name)
        feed_back = utils.goal_keeper(patch)
        if feed_back['build_status'] == 'pass' and feed_back['test_status'] == 'pass':
            break
        elif feed_back['build_status'] == 'pass' and feed_back['test_status'] == 'fail':
            # TODO: process pov_results and add it to the prompt
            # harness_fdbk = feed_back['test_output']
            continue
        elif feed_back['build_status'] == 'fail':
            # harness_fdbk = feed_back['build_output']
            continue
        if iter > 20:
            break
        iter += 1
