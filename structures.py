
class Project:
    def __init__(self, input_json):
        '''
        {
            "project_name": "challenge-001-exemplar-cp",
            "commmit": "123456abcdef",
            "file_name": "/path/to/example.c",
            "function_name": "example_func",
            "line_number": [213,256],
        }
        '''
        self.project_name = input_json["project_name"]
        self.commit = input_json["commit"]
        self.base_directory = input_json["base_directory"]
        self.project_path = f"/tmp/{self.project_name}{self.base_directory}/"
        self.file_name = input_json["file_name"]
        self.function_name = input_json["function_name"]
        self.line_number = input_json["line_number"]
        with open(f".{self.project_path}{self.file_name}", "r") as f: # TODO: how to identify src and kernel?
            text = f.readlines()
            self.code = "".join(text[self.line_number[0]:self.line_number[1]])
            self.prefix =  "".join(text[self.line_number[0]-50:self.line_number[0]])
            self.sufix =  "".join(text[self.line_number[1]:self.line_number[1]+50])