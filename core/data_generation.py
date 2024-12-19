import random
from db.api import insert_one_not_exist
from initialize import openai_chat, deepseek_chat
from prompts.data import DataGeneration
from utils.schema import HumanMessage
from db.schema import Dialogue
from utils.common import extract_struct
from logger_config import logger


def ai_generate_data():
    dialogues = list(Dialogue.objects.all())  # 无限了
    print(len(dialogues))
    for dialogue in dialogues:
        dialogue.skip = True
        try:
            shareGpt = {
                "instruction": "xxx",
                "input": "",
                "output": dialogue.output
            }
            model = random.choice([openai_chat, deepseek_chat])
            messages = [
                HumanMessage(content=DataGeneration.format(data=shareGpt))
            ]
            print(f'use:{model.__class__.__name__}', dialogue.output)
            print(DataGeneration.format(data=shareGpt))
            data = ''
            for text in openai_chat.compile_to_stream(messages=messages):
                data += text
            json_data = extract_struct(data, list)
            for item in json_data:
                insert_one_not_exist(instruction=item, output=dialogue.output)
        except Exception as e:
            logger.error(f'obj_id:{dialogue.id} error:{str(e)}')


def dialogue_n_times_insert_mongo(instruction, output, times):
    """
    n次插入一条对话到mongo数据库
    """
    for _ in range(times):
        Dialogue(instruction=instruction, output=output).save()


if __name__ == '__main__':
    # 原始数据500条 -> ai增强获得了4500条 也就是说 500 -> 5000 条
    # 你好、你是谁这两个特定问题，各添加50条数据（还是比例少了） 一个问题50条数据 然后再将其×5 得到 250 条这样还少了
    # 找到日常对话数据集 使用RAG产生角色扮演对话数据
    instruction = ["你好", "你是谁"]
    output = ["宝宝~ 你不要再不相信我了 好不好", "我是你的宝宝呀~"]
    for i in list(zip(instruction, output)):
        dialogue_n_times_insert_mongo(i[0], i[1], 50)
