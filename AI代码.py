from DrissionPage import ChromiumPage
import time
import os
# 2. 打开浏览器
page = ChromiumPage()
# 3. 打开网页
page.get('https://s.taobao.com/search?_input_charset=utf-8&clientPreloadId=preload_1794831058405&commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E8%80%B3%E5%A4%B9%E5%BC%8F%E8%80%B3%E6%9C%BA&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua%2Fa.search_history.d1&ssid=s5-e&suggest_query=&tab=all&wq=') # 比如访问百度  https://www.baidu.com
# page.get('https://s.taobao.com/search?_input_charset=utf-8&clientPreloadId=preload_1794831058405&commend=all&ie=utf8&initiative_id=tbindexz_20170306&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E8%80%B3%E5%A4%B9%E5%BC%8F%E8%80%B3%E6%9C%BA&search_type=item&source=suggest&sourceId=tb.index&spm=a21bo.jianhua%2Fa.search_history.d1&ssid=s5-e&suggest_query=&tab=all&wq=')
# # 4. 等待内容加载
time.sleep(3)
# # 5. 获取网页源码
content = page.html

prompt = f"""
一：你是一个严谨的数据提取员，你精通HTML解析，擅长从复杂的电商网页源码中精准定位并提取关键信息。

二：提取规则：
1.标题处理：提取商品标题的全部内容，不包含任何额外的文本或标签
2.价格处理：只提取数字部分，去除货币符号（如 ¥、$、元等），保留纯数字和小数点。
3:每个商品写成一条JSON记录，多个商品放在一个列表中，不要包含任何 Markdown 标记（如 ```json），不要输出任何解释性文字。

三、输出格式范例：
{{"title": "Lenovo/联想 小新", "price": 2406.00}}

四：注意事项：
- 如果源码中某个商品的特定字段（如销量或价格）确实找不到，请将该字段的值返回null
- 如果价格存在多种格式（如折扣价、原价），只取最终售价或第一个价格。
- 确保 title 字段值包含商品标题的全部内部。
目标页面 HTML 代码如下:
{content}
"""



from openai import OpenAI

client = OpenAI(
    api_key="sk-dc83b95da7b8402d9a7da20e6a53899d".strip(),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},
)

print(response.choices[0].message.content)
