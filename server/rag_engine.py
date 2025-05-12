from openai import OpenAI
from enum import Enum
from typing import List
from Embedding import retrieve_advices
import json

openai_client = OpenAI(api_key="enter your api key")

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

    structure_guide = "Please structure your answer as follows:\n"
    section_num = 1
    if TaskType.legal_statute_search in task:
        structure_guide += f"{section_num}. **Legal Statutes:** Cite applicable legal provisions.\n"
        section_num += 1
    if TaskType.similar_case_retrieval in task:
        structure_guide += f"{section_num}. **Similar Cases:** Identify any cases from the context that relied on the same or similar statutes (e.g., 405 ILCS 5). For each case, provide:\n"
        structure_guide += "   - Case name and court\n"
        structure_guide += "   - Key facts of the case\n"
        structure_guide += "   - What statute was applied\n"
        structure_guide += "   - How the court reasoned and ruled\n"
        structure_guide += "   - Why it is relevant to the user's question\n"
        section_num += 1
    structure_guide += f"{section_num}. **Legal Analysis:** Relate facts to legal standards.\n"
    section_num += 1
    structure_guide += f"{section_num}. **Conclusion:** Summarize your reasoning based on context.\n"

    disclaimer = (
        "Before using the retrieved legal context, first evaluate whether it is relevant to the user's question. "
        "If the context appears unrelated, ignore it."
        "In that case, answer all required questions using your own legal knowledge instead. "
    )

    prompt = f"""You are an experienced legal analyst trained in U.S. case law. You are assisting in evaluating legal cases based on statutory criteria and precedent.
            Please perform the following tasks:
            {task_description}

            {structure_guide}

            Here is the retrieved legal context:
            {context}

            User's question:
            {user_question}

            {disclaimer}

            Answer in JSON format with keys `legal_statutes`, `similar_cases`, `legal_analysis`, and `conclusion`:
            Each key must be completed using either the retrieved legal context(if it is relevant to the user's question based on your evaluation) or your own legal knowledge.

            """

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        parsed = json.loads(response.choices[0].message.content.strip())
    except Exception:
        parsed = {"raw_answer": response.choices[0].message.content.strip()}

    return parsed
