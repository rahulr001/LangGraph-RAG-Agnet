from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from utils import local_llm
from retriever import retriever
from prompts import retrival_prompt, rag_generator_prompt, hallucination_grade_prompt, answer_prompt, question_prompt


llm = ChatOllama(model=local_llm, format="json", temperature=0)



retrieval_grade_generator = retrival_prompt | llm | JsonOutputParser()
question = "agent memory"
docs = retriever.invoke(question)
doc_txt = docs[1].page_content
print(retrieval_grade_generator.invoke({"question": question, "document": doc_txt}))


rag_generator = rag_generator_prompt | llm | StrOutputParser()

# Run
question = "agent memory"
docs = retriever.invoke(question)
generation = rag_generator.invoke({"context": docs, "question": question})
print(generation)


hallucination_grade_generator = hallucination_grade_prompt | llm | JsonOutputParser()
hallucination_grade_generator.invoke({"documents": docs, "generation": generation})


answer_grader = answer_prompt | llm | JsonOutputParser()
answer_grader.invoke({"question": question, "generation": generation})


question_router = question_prompt | llm | JsonOutputParser()
question = "llm agent memory"
docs = retriever.invoke(question)
doc_txt = docs[1].page_content
print(question_router.invoke({"question": question}))