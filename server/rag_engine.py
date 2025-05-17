from openai import OpenAI
from enum import Enum
from typing import List
from Embedding import retrieve_advices
import json

openai_client = OpenAI(api_key="your api key")

class TaskType(str, Enum):
    legal_statute_search = "legal_statute_search"
    similar_case_retrieval = "similar_case_retrieval"
    general_answer = "general_answer"

# Core logic to construct prompt and call LLM
def generate_structured_answer(task: List[TaskType], user_question: str):
    context = retrieve_advices(user_question)
    # context = ""

    task_description = "- Provide a structured legal analysis based on the user's question and the retrieved legal context.\n"
    if TaskType.legal_statute_search in task:
        task_description = "- Identify any relevant legal statutes or codes that may apply.\n" + task_description
    if TaskType.similar_case_retrieval in task:
        task_description = "- Retrieve and summarize any similar legal cases that rely on the same or similar legal statutes.\n" + task_description

    # Build Markdown section headers based on selected tasks
    markdown_sections = []
    if TaskType.legal_statute_search in task:
        markdown_sections.append("## Legal Statutes")
    if TaskType.similar_case_retrieval in task:
        markdown_sections.append("## Similar Cases")
    markdown_sections.append("## Legal Analysis")
    markdown_sections.append("## Conclusion")
    section_instruction = "\n".join(markdown_sections)

    # Structure guide for the response
    disclaimer = (
        "Before using the retrieved legal context, first evaluate whether it is relevant to the user's question. "
        "If the context appears unrelated, ignore it."
        "In that case, answer all required questions using your own legal knowledge instead. "
    )

    prompt = f"""You are an experienced legal analyst trained in U.S. case law. You are assisting in evaluating legal cases based on statutory criteria and precedent.
            Please perform the following tasks:
            {task_description}

            Here is the retrieved legal context:
            {context}

            User's question:
            {user_question}

            {disclaimer}
            
            Please write the full answer in **Markdown format** using the following section headers:
            {section_instruction}

            Start each section with the corresponding Markdown heading (e.g., ## Legal Statutes), and ensure each section is well developed.
            Use bullet points, bolded statute names, and numbered case lists where appropriate. Do not output JSON. Return only Markdown text.

            Each key must be completed using either the retrieved legal context(if it is relevant to the user's question based on your evaluation) or your own legal knowledge.
            """

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    parsed = response.choices[0].message.content.strip()

    return parsed



