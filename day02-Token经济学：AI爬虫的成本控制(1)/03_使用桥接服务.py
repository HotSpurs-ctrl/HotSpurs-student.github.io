# 装好node.js 配置config.json   npm install  npm start启动桥
# 在打开的chrom把deepseek登录上

import requests

BASE_URL = "http://127.0.0.1:3010"
# 需要和config.json中填写的对上
anhao = "qiu_qiu_ni"

headers = {
    "Authorization": f"Bearer {anhao}",
    "Content-Type": "application/json",
}
Q = '圆圆 有空吗?'
payload = {
    "model": "deepseek",
    "messages": [
        {"role": "user", "content": Q}
    ],
}

res = requests.post(
    f"{BASE_URL}/v1/chat/completions",
    headers=headers,
    json=payload
)
res.raise_for_status()

print(res.json()["choices"][0]["message"]["content"])
