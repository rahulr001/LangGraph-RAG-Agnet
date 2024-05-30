from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict
from typing import List
from app.checkpoints import (web_search, retrieve, grade_documents, generate, 
                         route_question, decide_to_generate, grade_generation_v_documents_and_question)

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """

    question: str
    generation: str
    web_search: str
    documents: List[str]


workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("websearch", web_search) 
workflow.add_node("retrieve", retrieve) 
workflow.add_node("grade_documents", grade_documents) 
workflow.add_node("generate", generate) 


workflow.set_conditional_entry_point(
    route_question,
    {
        "websearch": "websearch",
        "vectorstore": "retrieve",
    },
)


workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "websearch": "websearch",
        "generate": "generate",
    },
)


workflow.add_edge("websearch", "generate")
workflow.add_conditional_edges(
    "generate",
    grade_generation_v_documents_and_question,
    {
        "not supported": "generate",
        "useful": END,
        "not useful": "websearch",
    },
)