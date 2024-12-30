import requests
import parsel
import re
import time
import csv
import random
# 打开 CSV 文件并写入标题行
with open('1-5页.csv', mode='w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)
    
    # 写入标题行（示例）
    writer.writerow(["标题", "信息", "价格", "电梯信息", "用水数据", "用电数据", "燃气数据"])

    # 爬取页面
    for page in range(6, 16):
        time.sleep(random.uniform(3, 7))
        url = f'https://zh.lianjia.com/zufang/pg{page}'
        user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'
]
# 请求头设置
        headers = {
    'User-Agent': random.choice(user_agents)
    }
        response = requests.get(url=url, headers=headers)
        print(response.text)
    # 检查请求是否成功
        if response.status_code == 200:
            print(f'Page {page} fetched successfully.')
        else:
            print(f'Failed to fetch page {page}. Status code: {response.status_code}')
            continue  # 如果请求失败，跳过本次循环，继续处理下一个页面
        # 数据解析
        selector = parsel.Selector(response.text)
        items = selector.css('.content__list--item--main')
        urls = selector.css('.content__list--item--main .content__list--item--title a::attr(href)').getall()
        print(f'Page {page}: items = {items}, urls = {urls}')
        
        
        # 遍历每一个匹配的元素
        for item, url1 in zip(items, urls):  # 使用 zip 来同时遍历 items 和 urls
            # 提取 content__list--item--title 的 a 标签文本
            title = item.css('.content__list--item--title a::text').get().strip()

            # 提取 content__list--item--des 中的 i 标签文本
            raw_info = item.css('.content__list--item--des *::text').getall()
            info_text = ''.join(raw_info).replace('/', '').strip()
            info_text1 = re.sub(r'\s+', ' ', info_text)  # 去掉多余的空格

            # 提取价格
            price = item.css('.content__list--item-price em::text').get()

            # 获取详细信息
            full_url = 'https://zh.lianjia.com' + url1  # 注意要加上完整的基础 URL
            response1 = requests.get(url=full_url, headers=headers)
            info_selector = parsel.Selector(response1.text)
            info_list = info_selector.css('.content__article__info ul li.fl.oneline::text').getall()

            # 清理信息中的多余空白
            info_list = [info.strip() for info in info_list if info.strip()]  # 移除空白字符

            # 提取详细信息（带检查防止越界）
            info_6 = info_list[6] if len(info_list) > 6 else '无电梯信息'
            info_8 = info_list[8] if len(info_list) > 8 else '无用水数据'
            info_9 = info_list[9] if len(info_list) > 9 else '无用电数据'
            info_10 = info_list[10] if len(info_list) > 10 else '无燃气数据'

            print(title, info_text1, price, info_6, info_8, info_9, info_10)
            # 写入 CSV 文件，每一行的数据为一条记录
            writer.writerow([title, info_text1, price, info_6, info_8, info_9, info_10])

print("Data has been written to csv")

   
   
    
   
   