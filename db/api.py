import json

from db.schema import Dialogue


def insert_one_not_exist(instruction, output):
    """
    插入一条不重复的数据。
    重复的定义是：instruction、output都与数据库某条数据相同
    """
    # 检查数据库中是否已经存在相同的 instruction 和 output
    if not Dialogue.objects(instruction=instruction, output=output):
        # 如果没有重复，就插入新文档
        dialogue = Dialogue(instruction=instruction, output=output)
        dialogue.save()
        print(f"Inserted: {instruction} -> {output}")
    else:
        print(f"Duplicate found: {instruction} -> {output}")


def delete_one_from_keyword(field, keyword):
    """
    删除一条包含敏感词的数据
    """
    Dialogue.objects(**{f'{field}__contains': keyword}).delete()


if __name__ == '__main__':
    path = '../example/final_data_example.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            instruction = item.get("instruction")
            output = item.get("output")
            insert_one_not_exist(instruction, output)
