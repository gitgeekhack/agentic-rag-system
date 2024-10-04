from app import anthropic_llm
from app.llm_integration import ask_llm
from langchain.agents import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import PromptTemplate

from app.tools import custom_calculator, wikipedia_search_tool, query_llm
from app.sarvam_integration import text_to_speech

tools = [custom_calculator, wikipedia_search_tool, query_llm]

def construct_agent():
    prompt_template = """Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
    """
    prompt = PromptTemplate(template=prompt_template)
    return create_react_agent(anthropic_llm, tools, prompt)

def is_greeting(query: str) -> bool:
    """Check if the query is a greeting."""
    greetings = ["hello", "hi", "greetings", "hey"]
    return any(greet in query.lower() for greet in greetings)

def process_agent_query(query: str, voice_enabled=False):
    """
    Process the query and decide whether to call the VectorDB, perform a calculation,
    or use voice features based on the user's input.
    """
    if is_greeting(query):
        response = "Hey there, how can I assist you today?"

    else:
        agent = construct_agent()
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,
                                       return_intermediate_steps=True)
        answer = agent_executor.invoke({
            "input": query
        })
        response = answer['output']

    # If voice is enabled, convert the response to speech
    if voice_enabled:
        audio_file_path = text_to_speech(response)
        return {"response": response, "audio": audio_file_path}
    else:
        return {"response": response}

def process_query(query:str, voice_enabled=False):
    response = ask_llm(query)

    # If voice is enabled, convert the response to speech
    if voice_enabled:
        audio_file_path = text_to_speech(response)
        return {"response": response, "audio": audio_file_path}
    else:
        return {"response": response}