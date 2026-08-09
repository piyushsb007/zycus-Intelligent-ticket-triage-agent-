# =============================================================================================
# LLM-as-Judge using LangChain + Groq
# Change only MODEL_NAME and the API key to switch models.
# =============================================================================================

import json
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Configuration
MODEL_NAME = os.getenv("JUDGE_MODEL", "llama-3.1-8b-instant")

llm = ChatGroq(
    model=MODEL_NAME,
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

# Prompt template

prompt = ChatPromptTemplate.from_template(
    """
You are an evaluation judge.

Task: {task_name}
Test Case: {test_id}

Output:
{output_text}

Evaluate whether the output is reasonable, factually consistent,
and sufficiently complete.

Return ONLY valid JSON in this exact format:
{{
  "pass": true,
  "score": 0.0,
  "reason": "short explanation"
}}
"""
)

# Create reusable LangChain chain
judge_chain = prompt | llm

# Judge function
def judge_output(task_name: str, test_id: str, output_text: str):
    """
    Run the LLM judge and return a dictionary.
    """

    try:
        response = judge_chain.invoke({
            "task_name": task_name,
            "test_id": test_id,
            "output_text": output_text
        })

        return json.loads(response.content)

    except Exception as e:
        return {
            "pass": False,
            "score": 0.0,
            "reason": f"LLM judge error: {str(e)}"
        }