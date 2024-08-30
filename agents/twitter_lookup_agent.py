import os

from langchain import hub
# hub is to download pre-made prompts

from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
# create_react_agent takes a llm as an input and outputs an agent
# AgentExecutor is the runtime of the agent. It is going to receive our prompts and instructions of what to do

from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv
from tools.tools import get_profile_url_tavily

load_dotenv()

def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )
    template = """
           given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username
           In Your Final answer only the person's username"""

    # The LLM can extract the username from the Twitter profile page by leveraging its inherent text processing capabilities,
    # understanding of common URL structures, and the instructions provided in the prompt.
    # Even without a dedicated tool for extracting usernames, the LLM can infer and extract the correct information based on
    # its training and the patterns it has learned.

    # In an ideal case, we would also have a tool to extract the twitter username from the twitter profile page

    prompt_template = PromptTemplate(template=template, input_variables = ['name_of_person'])

    tools_for_agent = [
        Tool(
            name="Crawl Google 4 twitter profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the Twitter Page URL",
        )
    ]
    # The description is very important and it has to be concise. The llm uses the description to decide whether
    # to use the tool or not.
    # The agent invokes the tool according to it's reasoning engine.

    react_prompt = hub.pull("hwchase17/react")
    # hw stands for harrison chase. react is a super popular prompt used for ReAct prompting.
    # The ReAct prompt is a prompt that is sent to the llm. It will include our tool names and our tool
    # descriptions and what we want our agents to do.
    # react_prompt is a type of prompting strategy that the llm uses to arrive at the answer.

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
    # agent_executor runs the agent in loops.

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    twitter_username = result["output"]
    return twitter_username

if __name__ == "__main__":
    twitter_username = lookup(name = "Elon Musk")
    print(twitter_username)
