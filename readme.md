# AI夸夸机器人

## 原始数据清洗：

去重与去噪：去除重复、不相关、语义不完整的评论，减少无效数据。
敏感信息过滤：通过正则表达式匹配和关键词过滤，删除含有敏感或不合适内容的评论。

## AI生成QA对话：

撰写与任务相关的 prompt，并通过并发请求 API，生成指定主题的问答对话内容。（基于夸夸数据集、抖音评论数据）
生成采用 Alpaca 格式文件，包含以下字段：
Instruction：用户的输入指令或发起的对话内容。
Output：模型针对输入的具体回答。
System：描述模型的任务指令，用于控制生成内容的风格和语气。