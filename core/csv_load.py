import csv
from typing import List, Tuple


def get_qa_from_csv(path, num=None) -> List[Tuple[str, str]]:
    aq = []
    with open(path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # 跳过表头
        next(reader)
        # 获取前 num 行，若 num 为 None 则读取整个文件
        for i, row in enumerate(reader):
            if num is not None and i >= num:
                break
            data = row[0].split("|")
            question, answer = data
            aq.append((question.strip(), answer.strip()))
    return aq


if __name__ == '__main__':
    # 使用函数
    file_path = r'D:\project\dataset_maker\data\other\train.csv'
    qa = get_qa_from_csv(file_path, num=10)

    # 打印结果
    for question, answer in qa:
        print(f'{question} {answer}')
