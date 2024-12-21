from openai import OpenAI


class OpenAIChat:
    def __init__(self, model, apikey, **kwargs):
        self.model = model
        self.apikey = apikey
        self.kwargs = kwargs

    def stream(self, messages):
        client = OpenAI(api_key=self.apikey, base_url="https://api.chatanywhere.tech/v1", )
        stream = client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            **self.kwargs
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    async def chat_complete(self, messages):
        resp = ''
        for text in self.compile_to_stream(messages):
            print(text, end='')
            resp += text
        return resp

    def compile(self, messages):
        return [m.json for m in messages]

    def compile_to_stream(self, messages):
        for text in self.stream(self.compile(messages)):
            yield text


if __name__ == '__main__':
    chat = OpenAIChat('gpt-4o-mini', 'sk-xxxxxx')
    messages = [
        {"role": "user", "content": "你好"}
    ]
    response = chat.stream(messages=messages)
    for r in response:
        print(r, end='')
