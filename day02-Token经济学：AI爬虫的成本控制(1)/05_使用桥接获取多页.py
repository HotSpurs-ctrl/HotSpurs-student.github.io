#1：导入DrissionPage的方法
from DrissionPage import  ChromiumPage
import time
import json
## 2.打开浏览器
page=ChromiumPage()
page_num = range(1,4)
datas = []
for i in page_num:
    url = f'https://www.dianping.com/search/keyword/1/0_%E9%A4%90%E5%8E%85/r836p{i}'
    #3 打开网页
    page.get('https://www.dianping.com/search/keyword/1/0_%E9%A4%90%E5%8E%85/r836')
    #  4 加载数据
    time.sleep(3)

    # 5 获取当前网页的源码
    # content = page.html
    # body = page.ele('tag:body').html
    try:
        body = page.ele('xpath://*[contains(@class,"star_")]/ancestor::ul[1]').html
    except Exception:
        try:
            body = page.run_js('''
                var s = document.querySelector('[class*="star_"]');
                var ul = s ? s.closest('ul') : null;
                return ul ? ul.outerHTML : document.body.innerHTML;
            ''')
        except Exception:
            body = page.ele("tag:body").html
    print(f"发送给AI的HTML长度：{len(body)} 字符")
    # 6 提出需求
    prompt=f"""
一、你是一个严谨的数据提取员。你精通 HTML 解析，擅长从复杂的餐饮商家列表网页源码中精准定位并提取关键信息。

二、提取规则：
1. 名称处理：提取餐厅名称的全部内容，不包含额外的标签、评分、优惠标识等无关信息。
2. 评分处理：优先提取餐厅评分对应的 HTML class 类名。若评分区域包含 star_XX 格式的类名，则提取其中的数字并除以 10，得到餐厅评分。例如，star_40 对应 4.0 分，star_45 对应 4.5 分。如果找不到符合规则的评分类名，则返回 null。
3. 人均消费：提取餐厅的人均消费金额，只保留数字，去除货币符号（如 ¥、￥、元等）。如果源码中没有人均消费信息，返回 null。
4. 菜系：提取餐厅所属的菜系或餐饮类型，例如西餐、本帮菜、日本料理、意大利菜等。如果没有相关信息，返回 null。
5. 地址：提取餐厅所在的商圈或地址信息，例如“新天地/马当路”。如果没有相关信息，返回 null。
6. 链接：提取餐厅详情页的完整 URL 链接，优先提取 HTML 中该餐厅对应的详情页链接，并将相对路径转换为完整 URL。如果源码中没有详情页链接，返回 null。
7. 输出格式：每个商品写成一条JSON记录，多个商品放在一个列表中，不要包含任何 Markdown 标记（如 ```json），不要输出任何解释性文字。

三、输出格式范例：
[
  {{
    "name": "Journal Standard Foodies(上海新天地广场店)",
    "rating": 3.5,
    "average_price": 120,
    "cuisine": "西餐",
    "address": "新天地/马当路",
    "link": "https://example.com/restaurant/123"
  }}
]

四、注意事项：
- 如果源码中某个餐厅的特定字段找不到，请将该字段的值返回 null。
- 每家餐厅的名称、评分、人均消费、菜系、地址和链接必须来自同一家餐厅对应的 HTML 区域，禁止混淆不同餐厅的数据。
- 数字字段使用数字类型，不要将数字转换成字符串；缺失时使用 null。
- 字符串字段使用字符串类型；缺失时使用 null。
- 不得根据图片、常识或其他餐厅的信息猜测缺失字段。
- 确保输出为合法的 JSON 数组，可以直接使用 Python 的 json.loads() 解析。
- 如果页面中没有任何餐厅信息，输出空数组：[]。

目标页面 HTML 代码如下：
{body}
"""

    import requests

    BASE_URL = "http://127.0.0.1:3010"
# 需要和config.json中填写的对上
    anhao = "qiu_qiu_ni"

    headers = {
    "Authorization": f"Bearer {anhao}",
    "Content-Type": "application/json",
}

    payload = {
    "model": "deepseek",
    "messages": [
        {"role": "user", "content": prompt}
    ],
}

    res = requests.post(
    f"{BASE_URL}/v1/chat/completions",
    headers=headers,
    json=payload
)
    res.raise_for_status()

    data = res.json()["choices"][0]["message"]["content"]
    result = json.loads(data)
    print(result)
    datas.append(result)
import pandas
df = pandas.DataFrame(datas)
df.to_csv('餐厅数据_3.csv', index=False)
