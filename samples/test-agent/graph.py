from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic.dataclasses import dataclass
from uipath.tracing import traced


@dataclass
class TestInput:
    message: str


@dataclass
class TestOutput:
    result: str


@traced(name="process")
async def process(input: TestInput) -> TestOutput:
    """
    Simple test agent that echoes the input message.
    """
    result = f"Test agent received: {input.message}"
    return TestOutput(result=result)


builder = StateGraph(state_schema=TestInput, input=TestInput, output=TestOutput)

builder.add_node("process", process)
builder.add_edge(START, "process")
builder.add_edge("process", END)

graph = builder.compile()

