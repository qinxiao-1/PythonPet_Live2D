

# coding=utf-8
import requests
import json
import urllib3

urllib3.disable_warnings()
DeepseekAPI = '0fVLRMeB2H4oMm5EWvON18Vb4QQCN3qO8fQklA2s2CTeA_oPLZ7wR6wZuyMdw9yMGHWrcN1S-vsJI8H214wRXQ'

if __name__ == '__main__':
    url = "https://infer-modelarts-cn-southwest-2.modelarts-infer.com/v1/infers/707c01c8-517c-46ca-827a-d0b21c71b074/v1/chat/completions"

    # Send request.
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer yourApiKey' # 把yourApiKey替换成真实的API Key
    }
    data = {
        "model": "DeepSeek-V3",
        "max_tokens": 20,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "你好"}
        ],
        # 是否开启流式推理, 默认为False, 表示不开启流式推理
        "stream": False,
        # 在流式输出时是否展示使用的token数目。只有当stream为True时改参数才会生效。
        # "stream_options": { "include_usage": True },
        # 控制采样随机性的浮点数，值较低时模型更具确定性，值较高时模型更具创造性。"0"表示贪婪取样。默认为1.0。
        "temperature": 1.0
    }
    resp = requests.post(url, headers=headers, data=json.dumps(data), verify=False)

    # Print result.
    print(resp.status_code)
    print(resp.text)
