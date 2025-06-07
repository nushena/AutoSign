from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.chatanywhere.tech/v1")
)
# 非流式响应
def gpt_4o_mini_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    # print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# if __name__ == '__main__':
#     messages = [{'role': 'user','content': '鲁迅和周树人的关系'},]
#     # 非流式调用
#     gpt_4o_mini_api(messages)

def getVersion():
    # 你要想不更新就可以改成999999999999
    return '202506062208'