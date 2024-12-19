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


if __name__ == '__main__':
    # Dataset().create_dataset_from_dir(input_path=r'D:\project\MediaCrawler\example\target')
    Dataset().create_dataset_from_mongo()
