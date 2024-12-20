from openai import OpenAI
from openai import AsyncOpenAI
import openai


class DeepSeekChat:
    def __init__(self, model, apikey, **kwargs):
        self.model = model
        self.apikey = apikey
        self.kwargs = kwargs

    def stream(self, messages):
        client = OpenAI(api_key=self.apikey, base_url="https://api.deepseek.com/beta", **self.kwargs)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        for i in response:
            yield i.choices[0].delta.content

    async def async_stream(self, messages):
        client = AsyncOpenAI(api_key=self.apikey, base_url="https://api.deepseek.com/beta", **self.kwargs)
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )
        async for i in response:
            yield i.choices[0].delta.content

    # 聊天完成
    def chat_complete(self, messages):
        resp = ''
        for text in self.compile_to_stream(messages):
            resp += text
        return resp

    def compile(self, messages):
        return [m.json for m in messages]

    def compile_to_stream(self, messages):
        for text in self.stream(self.compile(messages)):
            yield text

    async def async_compile_to_stream(self, messages):
        resp = ''
        async for text in self.async_stream(self.compile(messages)):
            resp += text
        return resp

    async def chat_complete_async(self, messages):
        resp = ''
        for text in self.compile_to_stream(messages):
            resp += text
        return resp

    def ask(self, messages):
        return self.log_stream(self.stream(messages=[m.json for m in messages]))

    def log_stream(self, generator):
        text = ''
        for r in generator:
            text += r
            print(r, end='')
        return text


if __name__ == '__main__':
    chat = DeepSeekChat('deepseek-chat', "sk-8bc747fbd79841349075a3cd342bf324")
    messages = [
        {"role": "user", "content": "hello"}
    ]
    response = chat.stream(messages)
    for r in response:
        print(r, end='')
