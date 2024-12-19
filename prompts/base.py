from langchain.prompts import PromptTemplate


class PromptBase:
    prompt = 'you are a helpful assistant.'
    output = ''

    @classmethod
    def format(cls, **kwargs):
        prompt_template = PromptTemplate.from_template(cls.prompt)
        if not cls.output:
            cls.output = ''
        return prompt_template.format(**kwargs) + cls.output
