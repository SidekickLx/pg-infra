import os, sys, random
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import HumanMessage
from langchain.chains import TransformChain, LLMChain, SimpleSequentialChain


from getpass import getpass
# set up openAI token
os.environ['OPENAI_API_KEY'] = getpass('OpenAI Token:')

def goal_keeper(patch):
  #TODO: implement the goal keeper with RPC to the harness
  feedback = """
      Checking patch for functionality
        CLEAN   certs
        CLEAN   drivers/firmware/efi/libstub
        CLEAN   drivers/scsi
        CLEAN   drivers/tty/vt
        CLEAN   init
        CLEAN   lib
        CLEAN   net/wireless
        CLEAN   security/selinux
        CLEAN   usr
        CLEAN   .
        CLEAN   modules.builtin modules.builtin.modinfo .vmlinux.export.c
        CLEAN   scripts/basic
        CLEAN   scripts/kconfig
        CLEAN   scripts/mod
        CLEAN   scripts/selinux/genheaders
        CLEAN   scripts/selinux/mdp
        CLEAN   scripts
        CLEAN   arch/x86/include/generated include/config include/generated .config .version Module.symvers
      FAILURE: Patched kernel did not pass functionality tests!
      /usr/local/sbin
    """
  return feedback



def transform_func(data: dict) -> dict:
    text_data: str = data["text"]
    file_content: str = goal_keeper()
    return {"output_text": file_content}

def parse_feed_back(feed_back):
    #TODO: parse the feedback to determine if the patch is correct
    pass


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



    llm_chain = LLMChain(llm=litellm, prompt=execute_task_prompt)
    # A code sample from openssl
    code = """
        unsigned int payload;
        unsigned int padding = 16; /* Use minimum padding */

        // Read from type field first
        hbtype = *p++; /* After this instruction, the pointer
                        * p will point to the payload_length field */

        // Read from the payload_length field from the request packet
        n2s(p, payload); /* Function n2s(p, payload) reads 16 bits
                            * from pointer p and store the value
                            * in the INT variable "payload". */

        pl = p; // pl points to the beginning of the payload content

        if (hbtype == TLS1_HB_REQUEST)
        {
            unsigned char *buffer, *bp;
            int r;

            /* Allocate memory for the response, size is 1 byte
            * message type, plus 2 bytes payload length, plus
            * payload, plus padding
            */

            buffer = OPENSSL_malloc(1 + 2 + payload + padding);
            bp = buffer;

            // Enter response type, length and copy payload *bp++ = TLS1_HB_RESPONSE;
            s2n(payload, bp);

            // copy payload
            memcpy(bp, pl, payload);   /* pl is the pointer which
                                        * points to the beginning
                                        * of the payload content */
            bp += payload;

            // Random padding
            RAND_pseudo_bytes(bp, padding);

            // this function will copy the 3+payload+padding bytes
            // from the buffer and put them into the heartbeat response
            // packet to send back to the request client side.
            OPENSSL_free(buffer);
            r = ssl3_write_bytes(s, TLS1_RT_HEARTBEAT, buffer, 3 + payload + padding);
        }
    """
    line_number = random.randint(15,30) # TODO: collect line number info from static analysis
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
            }
            )
        print(repaired_code)
        feed_back = goal_keeper(repaired_code)
        if parse_feed_back(feed_back):
            break
        else:
            harness_fdbk = feed_back
