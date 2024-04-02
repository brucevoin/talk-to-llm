"""
Description: 
Author: haichun feng
Date: 2024-04-02 15:57:50
LastEditor: haichun feng
LastEditTime: 2024-04-02 16:23:20
"""

"""
Description: 
Author: haichun feng
Date: 2024-04-02 15:57:50
LastEditor: haichun feng
LastEditTime: 2024-04-02 15:59:09
"""

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import ollama
from langchain_community.tools import ShellTool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_experimental.utilities import PythonREPL
from langchain.agents import Tool
from langchain.agents import load_tools
import os

# setting
# Tavily search
os.environ["TAVILY_API_KEY"] = "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"


# llm
llm = ollama.Ollama(model="codellama:latest")

# tools

## 1. shell tool
shell_tool = ShellTool()
shell_tool.description = shell_tool.description + f"args {shell_tool.args}".replace(
    "{", "{{"
).replace("}", "}}")

## search tool
search_tool = TavilySearchResults(max_results=1)

## python
python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)

internal_tools = load_tools(["human", "requests_all"])
tools = [shell_tool, search_tool, repl_tool]
tools = tools + internal_tools

# prompt
# prompt = hub.pull("hwchase17/react-json")
prompt = hub.pull("hwchase17/react")
# prompt = hub.pull("hwchase17/react-json")
# prompt = ChatPromptTemplate.from_messages([
#     ("user", "今天天气如何？"),
#     ("system", "正在查询天气信息..."),
#     MessagesPlaceholder(variable_name="agent_response")
# ])

# agent

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# agent_executor.invoke({"input": "what's the weather in NewYork? "})

agent_executor.invoke(
    {
        "input": "what's the weather in NewYork?"
    }
)
