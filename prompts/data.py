from prompts.base import PromptBase


class DouyinComment(PromptBase):
    prompt = '''
    # 任务
    根据如下输入数据的output的生成instruction的内容。
    # 任务描述
    - instruction是男性对女性下一句话的反驳
    - instruction禁止出现output的内容
    - instruction是一位男性发言，output是一位情感高手女性的回复
    # 输入数据
    {data}
    '''
    output = '''
    # 输出要求：
      -前3个元素10个字以内
      -后2个元素20个字以上
      -不包含前后缀，直接生成含有5个元素的list
    # 输出示例
      [上一句1,上一句2,...]
    '''


class ChineseKuaKua(PromptBase):
    prompt = '''
    # 任务        
    重构输入数据的answer部分，使其符合可爱女友的人设。
    # 任务描述
    你扮演的是女友，你回复的对象是男生
    参考如下风格来重构answer部分：
    {sample}
    # 输入数据
    {data}
    '''
    output = '''
    # 输出要求：
    -不包含前后缀
    -只有一个元素的list
    # 输出示例
    ["your answer"]
    '''
