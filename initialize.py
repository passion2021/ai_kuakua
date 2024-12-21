import os
from llm.deepseekchat import DeepSeekChat
from llm.openaichat import OpenAIChat

deepseek_chat = DeepSeekChat(model="deepseek-chat", apikey=os.getenv("DEEPSEEK_API_KEY"))
openai_chat = OpenAIChat(model="gpt-4o-mini", apikey=os.getenv("OPENAI_API_KEY"),
                         temperature=0.7)
