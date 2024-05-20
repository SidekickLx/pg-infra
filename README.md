# PG-INFRA

This is the repository for LLM-based program auto-repair.

To setup the environment:
```shell
#using conda
conda create --name <env_name> --file requirements.txt
```

```shell
#using pip
pip install -r requirements.txt
```

### LLM setup

Curretly support using a LiteLLM wrap with Langchian. Set openAI api key with
```shell
export OPENAI_API_KEY='your-api-key-here'
```
TODO: set up a LiteLLM server with multiple LLM service supported.


### Usage:

#### Input

```json
{
    "project_name": "linux_kernel",
    "commmit": "123456abcdef",
    "file_name": "/net/tipc/crypto.c",
    "function_name": "static bool tipc_crypto_key_rcv(struct tipc_crypto *rx, struct tipc_msg *hdr)",
    "line_number": [2278,2337],
}

```


#### local test

```shell
python program_repair_iterative.py 
```
or 
```shell
python program_repair_agent.py
```

#### through RPC

TODO


#### LLM Agent for program auto-repair: 




### How to Contribute

tools.py: tools for LLM Agent

goalkeeper_test_patch.py: dependencys for goalkeeper RPC.

utils.py: utils for the iterative code repair program.




