import os
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents.tools import Tool
from langchain.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from goalkeeper_test_patch import test_patch


@tool
def goal_keeper_caller(patch_name:str, tgt_proj:str="linux")->dict:
    """Call an external API to test the patch"""
    with open(patch_name, 'r') as f:
        patch = f.read()
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

class patchInput(BaseModel):
    # source_file: list[str] = Field(description="source file list for patch generation")
    target_file: list[str] = Field(description="target file list for patch generation")
    patch_name: str = Field(description="name of the patch file")


@tool("gen_patch", args_schema=patchInput)
def gen_patch(target_file, patch_name):
    """Generate patch file from source and target files"""
    try:
        os.system(f"git add {target_file}")
        os.system(f"git diff > {patch_name}") # TODO: handle file lists
        return patch_name
    except Exception as e:
        print(e)
        return None



