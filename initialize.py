from llm.deepseekchat import DeepSeekChat
from llm.openaichat import OpenAIChat
deepseek_chat = DeepSeekChat(model="deepseek-chat", apikey="sk-8bc747fbd79841349075a3cd342bf324")
openai_chat = OpenAIChat(model="gpt-4o-mini", apikey="sk-TceIO7gS8tr8FXXv5LeaWmDC2CEHqaKLRNm9MlvkGMSX8bdn",
                         temperature=0.7)
