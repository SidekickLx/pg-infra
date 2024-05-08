import os,sys, random
from getpass import getpass
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain, LLMChain
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain import PromptTemplate
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.chains.conversation.memory import ConversationBufferMemory

# set up openAI token
os.environ['OPENAI_API_KEY'] = getpass('OpenAI Token:')


if __name__ == "__main__":
    prefix = """
        You are a cybersecurity expert that is responsible to repair a vulnerable code.
        {code}
        Your task is to generate a code snippet that fix the vulerability. Do not output other irrelavent information!
        You can use following tools {pr_tools}
        Here are some useful information that can help you identify the vulerability. There will be an 'N/A' if the information is not availiable.
        Possible line number of the vulerability: {line_number}
        The type of the Vulnerability : {vul_type}
        You will also be provided with sample repairs from the previous iteration and the feedback from an auto-test program.
        sample repair: {reapired_code}
        feedback: {harness_fdbk}
        """
    suffix = """
        Begin! Remember to answer very politely.
        Previous conversation history:
        {chat_history}
        {agent_scratchpad}
        """

    pr_tools = []


    prompt = ZeroShotAgent.create_prompt(
        tools = [],
        prefix=prefix,
        suffix=suffix,
        input_variables=[
            "input",
            "agent_scratchpad",
            "chat_history",
        ],
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", input_key="code", output_key="output"
    )

    litellm = ChatLiteLLM(model="gpt-4-turbo")
    llm_chain = LLMChain(llm=litellm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain)
    agent_executor = AgentExecutor.from_agent_and_tools(
        tools = [],
        agent=agent,
        verbose=True,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )
    agent_executor.invoke(
    {"code":
    """
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
    }
    )