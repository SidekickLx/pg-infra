import os


def gen_diff_file(source_file, target_file, filename):
    try:
        os.system(f"diff -u {source_file} {target_file} > {filename}")
        return filename
    except Exception as e:
        print(e)
        return None

def load_code_need_to_fix(input_json):
    """
    Load the code snippet from the input json
    input_json: dict {
        "files": ["file1,c", "file2.c"],
        ""

    }
    """
    for file in input_json["files"]:
        if file.endswith(".c"):
            with open(file, "r") as f:
                return f.read()
    return 


