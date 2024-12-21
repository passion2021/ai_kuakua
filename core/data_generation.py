import json
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
    CONCURRENT_REQUESTS = 10

    def __init__(self, input_data_num):
        self.num = input_data_num
        self.semaphore = asyncio.Semaphore(self.CONCURRENT_REQUESTS)

    async def chinese_kuakua_from_csv(self, path):
        output_data = []
        data = get_qa_from_csv(path=path, num=self.num)
        results = await self.process_batches(data)
        with open('chinese_kuakua.json', 'w', encoding='utf-8') as f:
            for result in results:
                q, a = result
                sample = {
                    "instruction": q,
                    "input": "",
                    "output": a
                }
                output_data.append(sample)
            json.dump(output_data, f, ensure_ascii=False, indent=4)
        return results  # 返回最终的结果列表

    def prompt_wrapper(self, data):
        random_num = random.randint(500, 500 + self.num - 1)
        obj = Dialogue.objects.all()[random_num]
        sample = {
            'question': obj.instruction,
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
            messages = self.prompt_wrapper(data)
            # 限制并发数
            tasks.append(asyncio.create_task(self.fetch_data(data, messages, index)))

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

    async def fetch_data(self, data, messages, index):
        try:
            # 获取返回结果
            result = await deepseek_chat.async_compile_to_stream(messages)
            logger.info(f"Request {index} succeeded: {result}")
            return (data[0], result)
        except Exception as e:
            logger.error(f"Request {index} failed with exception: {str(e)}")
            return None


if __name__ == '__main__':
    path = r'D:\project\dataset_maker\data\other\train.csv'
    input_data_num = 4
    asyncio.run(AsyncAIGenerator(input_data_num=input_data_num).chinese_kuakua_from_csv(path))
