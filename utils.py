import os
import json
import difflib
from goalkeeper_test_patch import test_patch



def get_input_json():
    LOCAL_TEST = True
    if LOCAL_TEST:
        with open("will_received.json", "r") as f:
            return json.load(f)
    else:
        # TODO: get input from RPC
        pass


def download_project(project_name):
    """Download project from git"""
    repo_url = "https://github.com/Sashikode/"
    # git clone
    os.system(f"git clone {repo_url}{project_name}.git ./tmp/{project_name}")
    os.system(f"cd ./tmp/{project_name} && ./run.sh pull_source")




def gen_patch(project, repaired_func, patch_name):
    """Generate patch file from source and target files"""
    # print(f".{project.project_path}{project.file_name}")
    # print(repaired_func)
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


def goal_keeper(patch_name, tgt_proj="linux"):
    # TODO: generate patch
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