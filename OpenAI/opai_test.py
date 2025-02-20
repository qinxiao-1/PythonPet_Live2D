from openai import OpenAI


def request_openai(in_content):
    client = OpenAI(
        api_key="api_key",  # 填写提供的api_key
        base_url="http://61.157.13.79:11434/v1"  # 填写提供的base_url
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

if __name__ == '__main__':
    print(request_openai("python 使用 websocket 链接服务器并发送数据"))