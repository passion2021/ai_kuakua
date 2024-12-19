import json
import os
import re
from typing import Dict, List, Any, TypedDict
from settings import LOCAL_STORE_PATH


class Dialogue(TypedDict):
    dialogue: List[str]  # 必须的键，值是字符串列表
    father_id: str
    child_id: str
    aweme_id: str


class JsonParse:
    """
    处理MediaCrawler生成的评论json数据
    """

    def read_json(self, path):
        with open(LOCAL_STORE_PATH / path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f'read name={path}, count={len(data)}')
            return data

    def write_json(self, path, data):
        with open(LOCAL_STORE_PATH / path, 'w', encoding='utf-8') as f:
            print(f'write name={path}, count={len(data)}')
            json.dump(data, f, ensure_ascii=False, indent=4)

    def parse_father_comment(self, data: Dict | List):
        """
        获取父评论。
        """
        father_comments = []
        for item in data:
            if item.get('parent_comment_id') == "0":
                father_comments.append(item)
        self.write_json('father_comments.json', father_comments)
        return father_comments

    def review_data(self, data, count):
        for i in data[count:]:
            print(i['comment_id'], i['content'])

    def clean_comments(self, data: List[Dict[str, Any]]):
        new_data = []
        for comment in data:
            if comment['content']:
                comment['content'] = self.sub_at(comment)
                new_data.append(comment)
        self.write_json('clean_comments.json', new_data)
        return new_data

    def sub_at(self, comment):
        """
        移除@前缀。
        """
        content = comment['content']
        # 统计评论中 @ 的个数
        at_count = content.count('@')
        if at_count > 1:
            # 找到最后一个 @ 的位置
            last_at_index = content.rfind('@')
            # 移除最后一个@ 之前的文本 和 后面的人名
            content = re.sub(r'^@[^\s]+\s*', '', content[last_at_index:])
        elif at_count == 1:
            # 如果只有一个 @，直接移除 @ 和后面的人名
            content = re.sub(r'^@[^\s]+\s*', '', content)
        if content.count('@') > 0:
            # 一般这些数据的含金量也不高可以不要了
            print('content:', content, 'comment_id:', comment['comment_id'])
        return content

    def generate_dialogues(self, fathers, origin) -> List[Dialogue]:
        """
        父子评论组合生成QA对话。
        一条父评论对应多条子评论，生成多条QA对话。

        Args:
            fathers: 父评论列表
            origin: 混杂父子评论的爬虫原始数据
        """
        dialogues = list()
        for father in fathers:
            father_id = father['comment_id']
            for comment in origin:
                if comment['content'] and comment['parent_comment_id'] == father_id:
                    dialogue = Dialogue(
                        dialogue=[father['content'], comment['content']],
                        father_id=father_id,
                        child_id=comment['comment_id'],
                        aweme_id=comment['aweme_id']
                    )
                    dialogues.append(dialogue)
        self.write_json("dialogue.json", dialogues)
        return dialogues

    def keyword_filter(self, data: List[Dialogue], keyword: list) -> List[Dialogue]:

        new_data = []
        for key in keyword:
            for comment in data:
                if key in comment['dialogue'][1]:
                    new_data.append(comment)
        self.write_json('new_dialogue.json', new_data)
        return new_data

    def work_flow(self, path: str, keyword: list = None):

        origin_data = self.read_json(path)
        clean_data = self.clean_comments(origin_data)
        if os.path.isfile('father_comments.json'):
            father_comments = self.read_json('father_comments.json')
        else:
            father_comments = self.parse_father_comment(clean_data)
        dialogue = self.generate_dialogues(father_comments, clean_data)
        if not keyword:
            return dialogue
        new_dialogue = self.keyword_filter(dialogue, keyword)
        return new_dialogue


if __name__ == '__main__':
    keyword = ['宝', '哥', '喜欢']
    origin_data_path = r'D:\project\MediaCrawler\data\douyin\json\detail_comments_2024-12-19.json'
    parse = JsonParse()
    parse.work_flow(origin_data_path, keyword)
