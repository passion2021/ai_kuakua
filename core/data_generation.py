import random
from db.api import insert_one_not_exist
from initialize import openai_chat, deepseek_chat
from prompts.data import DataGeneration
from utils.schema import HumanMessage
from db.schema import Dialogue
from utils.extract_tools import extract_struct
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


if __name__ == '__main__':
    ai_generate_data()
    # 原始数据500条 -> ai增强获得了4500条 也就是说 500 -> 5000 条
    # 你好、你是谁这两个特定问题，各添加50条数据（还是比例少了） 一个问题50条数据 然后再将其×5 得到 250 条这样还少了
    # 找到日常对话数据集 使用RAG产生角色扮演对话数据
    # 展示模型在微调前后的性能对比，包括准确率、响应时间等关键指标。
    # 可以通过截图或视频形式直观展示模型的效果
    # 数据标注：
    # 添加“情感标签”（如撒娇、关心、调侃）和“对话意图标签”（如提问、回答、安慰），便于模型学习对话风格。
    # 标注“父子对话关系”类型（如明确回答、偏题回应、情绪化表达）。。
