import os
import json
import difflib
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents.tools import Tool
from langchain.tools import tool
from langchain.pydantic_v1 import BaseModel, Field
from goalkeeper_test_patch import test_patch
from structures import Project

class goalKeeperInput(BaseModel):
    patch_name: str = Field(description="name of the patch file")
    tgt_proj: str = Field(description="target project name")


@tool("goal_keeper", args_schema=goalKeeperInput)
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
    project: Project = Field(description="target file list for patch generation")
    repaired_func: str = Field(description="repaired function")
    patch_name: str = Field(description="name of the patch file")
    


@tool("gen_patch", args_schema=patchInput)
def gen_patch(project, repaired_func, patch_name):
    """Generate patch file from source and target files"""
    try:
        repaired_func = repaired_func["text"]
        if repaired_func.startswith("```c"):
            repaired_func = repaired_func[5:-3]

        org_func = project.prefix + project.code + project.sufix
        repaired_func = project.prefix + repaired_func + project.sufix
        patch = difflib.unified_diff(org_func.splitlines(), repaired_func.splitlines(), lineterm='', fromfile="a"+project.file_name, tofile="b"+project.file_name)  
        with open(patch_name, 'w') as f:
            f.write("\n".join(patch)+"\n")
        return patch_name
    except Exception as e:
        print(e)
        exit(1)


@tool("download_project")
def download_project(project_name:str):
    """Download project from git"""
    repo_url = "https://github.com/Sashikode/"
    # git clone
    os.system(f"git clone {repo_url}{project_name}.git ./tmp/{project_name}")
    os.system(f"cd ./tmp/{project_name} && ./run.sh pull_source")


