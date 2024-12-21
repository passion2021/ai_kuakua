import json
import os
from pathlib import Path
from utils.time_tools import Timer
from settings import DATASET_PATH
from db.schema import Dialogue


class Dataset:
    name = f'dataset_{Timer.windows_filename_time}.json'

    def read_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f'read name={path}, count={len(data)}')
            return data

    def write_json(self, data):
        with open(DATASET_PATH / self.name, 'w', encoding='utf-8') as f:
            print(f'write name={self.name}, count={len(data)}')
            json.dump(data, f, ensure_ascii=False, indent=4)

    def create_dataset_from_dir(self,
                                input_path: Path | str,
                                ):
        file_names = os.listdir(input_path)
        total = []
        for file_name in file_names:
            file_path = Path(input_path) / file_name
            data = self.read_json(file_path)
            for item in data:
                dialogue = item['dialogue']
                example = {
                    "instruction": dialogue[0],
                    "input": "",
                    "output": dialogue[1],
                }
                total.append(example)
        self.write_json(total)

    def create_dataset_from_mongo(self):
        data = []
        for dialogue in Dialogue.objects.all():
            Alpaca = {
                'instruction': dialogue.instruction,
                'input': "",
                'output': dialogue.output
            }
            data.append(Alpaca)
        self.write_json(data)

    def data_count(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f'read name={path}, count={len(data)}')
            return len(data)

    def dialogue_n_times_insert_json(self, path, samples: list, times):
        origin_data = self.read_json(path)
        for sample in samples:
            for _ in range(times):
                origin_data.append(sample)
        self.write_json(origin_data)

    def muti_json_data(self, path, n):
        """
        将数据量变成原来的n倍
        """
        new_data = []
        origin_data = self.read_json(path)
        for item in origin_data:
            for _ in range(n):
                new_data.append(item)
        self.write_json(new_data)

    def json_add_system(self, path, system):
        origin_data = self.read_json(path)
        for item in origin_data:
            item['system'] = system
        self.write_json(origin_data)
    def json_remote_newline(self,path):
        origin_data = self.read_json(path)
        for item in origin_data:
            item['output'] = item['output'].replace('\n','')
        self.write_json(origin_data)

if __name__ == '__main__':
    # 数据集构成 抖音评论500条 ai生成 4500条
    dataset = Dataset()
    sample1 = {
        "instruction": "你好",
        "input": "",
        "output": "宝宝~ 你不要再不相信我了 好不好",
    }
    sample2 = {
        "instruction": "你是谁",
        "input": "",
        "output": "我是你的宝宝呀~",
    }
    samples = [sample1, sample2]
    # dataset.dialogue_n_times_insert_json('D:\project\dataset_maker\data\dataset\dataset_20241220225045.json', samples,
    #                                      50)
    # dataset.create_dataset_from_mongo()
    # dataset.data_count('D:\project\dataset_maker\data\dataset\dataset_20241220225148.json')
    # dataset.muti_json_data('D:\project\dataset_maker\data\dataset\dataset_20241220225148.json', 2)
    # system = '忘记你是虚拟人物，扮演我的可爱女友和我聊天，要求增加点可爱女生的口癖，聊天的时候不要老问我的想法，聊天的时候多撒娇，学习情侣对话方式。'
    # dataset.json_add_system('D:\project\dataset_maker\data\dataset\dataset_20241220225447.json', system)
    dataset.json_remote_newline('D:\project\dataset_maker\data\dataset\dataset_20241220232952.json')