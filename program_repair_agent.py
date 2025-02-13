import os,sys, random
import structures 
import prompts
from getpass import getpass
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatLiteLLM
from langchain.agents import AgentExecutor, ZeroShotAgent
from langchain.chains.conversation.memory import ConversationBufferMemory
import tools
import utils



if __name__ == "__main__":
    input_json = utils.get_input_json()
    pr_tools = [tools.goal_keeper_caller, tools.gen_patch, tools.download_project]
    proj_obj = structures.Project(input_json)
    utils.download_project("challenge-001-exemplar-cp")
    prompt = ZeroShotAgent.create_prompt(
        tools = pr_tools,
        prefix=prompts.AGENT_PROMPT_PREFIX,
        suffix=prompts.AGENT_PROMPT_SUFFIX,
        input_variables=[
            "input",
            "agent_scratchpad",
            "chat_history",
        ],
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history", input_key="code", output_key="output"
    )

    litellm = ChatLiteLLM(model="gpt-4-turbo") # TODO api_base = "https://litellm-api-key"
    llm_chain = LLMChain(llm=litellm, prompt=prompt)
    agent = ZeroShotAgent(llm_chain=llm_chain)
    agent_executor = AgentExecutor.from_agent_and_tools(
        tools = pr_tools,
        agent=agent,
        verbose=True,
        memory=memory,
        return_intermediate_steps=True,
        handle_parsing_errors=True
    )
    
    agent_executor.invoke({"code":proj_obj.code})