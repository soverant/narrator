import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

summarize_system_prompt = f"""
You are a Narrator who summarize a chat history for fast boarding
"""

def gai_summarizer(messages):
    text_to_summarize = "\n".join([msg[1] for msg in messages])
    chat_summarize_model = genai.GenerativeModel(model_name='gemini-1.5-flash-latest',
                                                 system_instruction=summarize_system_prompt)
    logger.debug("summary request: %s", text_to_summarize)
    summary = chat_summarize_model.generate_content(text_to_summarize)
    logger.debug("summary response: %s", summary.text)
    return summary.text

def openai_summarizer():
    return