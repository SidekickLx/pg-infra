
class Project:
    def __init__(self, input_json):
        '''
        {
            "project_name": "linux_kernel",
            "commmit": "123456abcdef",
            "file_name": "/path/to/example.c",
            "function_name": "example_func",
            "line_number": [213,256],
        }
        '''
        self.project_name = input_json["project_name"]
        self.commit = input_json["commit"]
        self.file_name = input_json["file_name"]
        self.function_name = input_json["function_name"]
        self.line_number = input_json["line_number"]
        with open(self.file_name, "r") as f:
            self.code = "\n".join(f.readlines()[self.line_number[0]:self.line_number[1]])
    
