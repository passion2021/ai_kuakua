import json
from core.csv_load import get_qa_from_csv

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


def delete_all_by_sensitive(field, keyword):
    """
    将包含敏感词的数据删除
    """
    count = Dialogue.objects(**{f'{field}__contains': keyword}).count()
    Dialogue.objects(**{f'{field}__contains': keyword}).delete()
    print(f"Deleted: {field} -> {keyword} count: {count}")


def delete_all_by_field(field, value):
    """
    将字段匹配特定内容的数据删除
    """
    count = Dialogue.objects(**{f'{field}': value}).count()
    Dialogue.objects(**{f'{field}': value}).delete()
    print(f"Deleted: {field} -> {value} count: {count}")


def update_all_data_field(field, old_value, new_value):
    """
    更新字段匹配特定内容的数据
    """
    count = Dialogue.objects(**{f'{field}': old_value}).count()
    Dialogue.objects(**{f'{field}': old_value}).update(**{f'{field}': new_value})
    print(f"Update: {field} -> {old_value} -> {new_value} count: {count}")


def trim_database_final(num):
    documents_to_delete = Dialogue.objects.order_by('-id')[:num]
    # 删除查询到的记录
    for doc in documents_to_delete:
        doc.delete()


if __name__ == '__main__':

    # path = r'D:\project\dataset_maker\core\chinese_kuakua.json'
    # with open(path, 'r', encoding='utf-8') as f:
    #     json_data = json.load(f)
    #     for item in json_data:
    #         insert_one_not_exist(instruction=item['instruction'], output=item['output'])

    # data = get_qa_from_csv(r'D:\project\dataset_maker\data\other\train.csv', 2500)
    # for question, answer in data:
    #     insert_one_not_exist(instruction=question, output=answer)

    trim_database_final(9)
