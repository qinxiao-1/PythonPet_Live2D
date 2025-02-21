from openai import OpenAI
from Config.resources import *

async def request_openai(in_content):
    client = OpenAI(
        api_key=OpenAIKey,  # 填写提供的api_key
        base_url=OpenAIUrl  # 填写提供的base_url
    )
    response = client.chat.completions.create(
        messages=[
            {'role': 'user', 'content': in_content},
        ],
        model='deepseek-r1:32b',
        stream=False
    )
    message_content = response.choices[0].message.content
    start = message_content.find("<think>")
    end = message_content.find("</think>") + len("</think>")
    return (message_content[:start] + message_content[end:]).replace('\n', '')
        
async def start_chat(text, on_finish):
    result = await request_openai(text)
    on_finish(result)

# if __name__ == '__main__':
#     print(request_openai("你好"))