import random
from db.api import insert_one_not_exist
from initialize import openai_chat, deepseek_chat
from prompts.data import DouyinComment
from utils.schema import HumanMessage
from db.schema import Dialogue
from utils.extract_tools import extract_struct
from logger_config import logger
from core.csv_load import get_qa_from_csv
import asyncio
from prompts.data import ChineseKuaKua


class AIGenerator:
    def douyin_from_mongo(self):
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
                    HumanMessage(content=DouyinComment.format(data=shareGpt))
                ]
                print(f'use:{model.__class__.__name__}', dialogue.output)
                print(DouyinComment.format(data=shareGpt))
                data = ''
                for text in openai_chat.compile_to_stream(messages=messages):
                    data += text
                json_data = extract_struct(data, list)
                for item in json_data:
                    insert_one_not_exist(instruction=item, output=dialogue.output)
            except Exception as e:
                logger.error(f'obj_id:{dialogue.id} error:{str(e)}')


class AsyncAIGenerator:
    CONCURRENT_REQUESTS = 2

    def __init__(self, input_data_num):
        self.num = input_data_num
        self.semaphore = asyncio.Semaphore(self.CONCURRENT_REQUESTS)

    async def chinese_kuakua_from_csv(self, path):
        data = get_qa_from_csv(path=path, num=self.num)
        results = await self.process_batches(data)
        return results  # 返回最终的结果列表

    def prompt_wrapper(self, data):
        random_num = random.randint(500, 500 + self.num - 1)
        obj = Dialogue.objects.all()[random_num]
        sample = {
            'question':obj.instruction,
            'answer': obj.output
        }
        data = {
            'question': data[0],
            'answer': data[1]
        }
        messages = [
            HumanMessage(content=ChineseKuaKua.format(data=data, sample=sample))
        ]
        return messages

    async def process_batches(self, data_list):
        tasks = []
        results = []  # 用来存储每个任务的结果
        # 分批处理数据
        for index, data in enumerate(data_list):
            data = self.prompt_wrapper(data)
            print(data)
            # 限制并发数
            tasks.append(asyncio.create_task(self.fetch_data(data, index)))

            # 每10个请求完成一个批次后再继续发送
            if len(tasks) >= self.CONCURRENT_REQUESTS:
                # 等待当前批次所有任务完成，并将结果收集到 results
                batch_results = await asyncio.gather(*tasks)
                results.extend(batch_results)  # 将本批次结果加入最终的结果列表
                tasks = []  # 清空任务列表，准备处理下一个批次

        # 处理最后剩余的请求
        if tasks:
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)  # 将剩余请求的结果加入最终结果列表

        return results  # 返回所有请求的结果

    async def fetch_data(self, data, index):
        try:
            # 获取返回结果
            result = await deepseek_chat.async_compile_to_stream(data)
            logger.info(f"Request {index} succeeded: {result}")
            return result
        except Exception as e:
            logger.error(f"Request {index} failed with exception: {str(e)}")
            return None


if __name__ == '__main__':
    path = r'D:\project\dataset_maker\data\other\train.csv'
    input_data_num = 5
    asyncio.run(AsyncAIGenerator(input_data_num=input_data_num).chinese_kuakua_from_csv(path))

    # 原始数据500条 -> ai增强获得了4500条 也就是说 500 -> 5000 条
    # 你好、你是谁这两个特定问题，各添加50条数据（还是比例少了） 一个问题50条数据 然后再将其×5 得到 250 条这样还少了
    # 找到日常对话数据集 使用RAG产生角色扮演对话数据
    # 展示模型在微调前后的性能对比，包括准确率、响应时间等关键指标。
    # 可以通过截图或视频形式直观展示模型的效果
    # 数据标注：
    # 添加“情感标签”（如撒娇、关心、调侃）和“对话意图标签”（如提问、回答、安慰），便于模型学习对话风格。
    # 标注“父子对话关系”类型（如明确回答、偏题回应、情绪化表达）。。
