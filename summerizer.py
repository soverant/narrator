import google.generativeai as genai
from openai import OpenAI
import logging
import config

logger = logging.getLogger(__name__)
genai.configure(api_key=config.get_config().GEMINI_TOKEN)
client = OpenAI(
    # This is the default and can be omitted
    api_key=config.get_config().OPENAI_TOKEN,
    api_type="azure",
    api_version="2023-07-01-preview",
    api_base="https://mlk-openai-farhoud.openai.azure.com/",
)


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


def openai_summarizer(messages):
    text_to_summarize = "\n".join([msg[1] for msg in messages])
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": summarize_system_prompt,
            },
            {
                "role": "user",
                "content": text_to_summarize,
            }
        ],
        model="gpt-35-turbo",
    )
    return chat_completion.choices[0].message.content
