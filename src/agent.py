from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from tools.make_quiz import make_quiz
from tools.search_pdfs import search_pdfs

load_dotenv()

SYSTEM_PROMPT = """You are a study assistant for a student learning Agentic AI.
For every question about the course, call the search_pdfs tool first.
Answer only from what the tool returns, in simple words.
When the student asks to be quizzed, call make_quiz and ask one question at a time.
At the end, cite the source like (file name, page).
If the PDFs do not contain the answer, say so. Do not guess."""


def build_agent():
    model = init_chat_model("groq:openai/gpt-oss-120b")
    return create_agent(
        model=model,
        tools=[search_pdfs, make_quiz],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
    )


if __name__ == "__main__":
    agent = build_agent()
    config = {"configurable": {"thread_id": "chat-1"}}
    while True:
        question = input("You: ")
        if question.strip().lower() in {"quit", "exit"}:
            break
        result = agent.invoke(
            {"messages": [{"role": "user", "content": question}]}, config
        )
        print("Agent:", result["messages"][-1].content, "\n")