import math
import numexpr
from pydantic import BaseModel, Field
from langchain.tools import tool
from app.llm_integration import ask_llm
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

class CalculatorToolArgsSchema(BaseModel):
    expression:str = Field(description="should be a mathematical expression")

@tool("calculator-tool", args_schema=CalculatorToolArgsSchema, return_direct=True)
def custom_calculator(expression: str) -> str:
    """Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {"pi": math.pi, "e": math.e}
    return str(
        numexpr.evaluate(
            expression.strip(),
            global_dict={},  # restrict access to globals
            local_dict=local_dict,  # add common mathematical functions
        )
    )

class WikipediaSearchToolArgsSchema(BaseModel):
    query:str = Field(description="should be a search query")

@tool("wikipedia-search-tool", args_schema=WikipediaSearchToolArgsSchema, return_direct=False)
def wikipedia_search_tool(query: str) -> str:
    """Search for the query on wikipedia
    """
    try:
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        return wikipedia.run(query)
    except Exception as e:
        return str(e)

class RetrievalToolArgsSchema(BaseModel):
    query:str = Field(description="should be a user query which is to be provided to LLM")

@tool("query-llm-tool", args_schema=RetrievalToolArgsSchema, return_direct=True)
def query_llm(query: str) -> str:
    """
    Asks LLM and gives the answer based on the context
    """
    return ask_llm(query)