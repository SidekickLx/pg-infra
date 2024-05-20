import os
import json
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
    try:
        with open(project.file_name, "r") as f:
            lines = f.readlines()
            # delete original function and insert the new one
            del lines[project.line_number[0]:project.line_number[1]]
            lines.insert(project.line_number[0], repaired_func.split("\n"))
        with open(project.file_name, "w") as f:
            f.write("\n".join(lines))
        os.system(f"git add {project.file_name}")
        os.system(f"git diff > {patch_name}") # TODO: handle file lists
        return patch_name
    except Exception as e:
        print(e)
        return None


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