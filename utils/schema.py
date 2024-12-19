from datetime import datetime


class BaseMessage:
    role_map = {
        'HumanMessage': 'user',
        'AIMessage': 'assistant',
        'SystemMessage': 'system',
        'SummaryMessage': 'user',
    }

    def __init__(self, content, create_time=None):
        if create_time is None:
            create_time = datetime.now()
        self.create_time = create_time
        self.content = content
        self.json = {'role': self.role_map[self.__class__.__name__], 'content': f"{self.content}"}

    def __repr__(self):
        return f"""\n{self.__class__.__name__}('''{self.content}''')\n"""



class HumanMessage(BaseMessage):
    type = 'human'


class AIMessage(BaseMessage):
    type = 'ai'


class SystemMessage(BaseMessage):
    type = 'system'


class SummaryMessage(HumanMessage):
    type = 'summary'


if __name__ == '__main__':
    print(dir(HumanMessage))
    print(HumanMessage('你好').__class__.__name__)
    print(HumanMessage('你好').content)
    print(HumanMessage('你好').json)
    print([HumanMessage('你好'), AIMessage('我不好')])
    print(SummaryMessage('你好').type)
