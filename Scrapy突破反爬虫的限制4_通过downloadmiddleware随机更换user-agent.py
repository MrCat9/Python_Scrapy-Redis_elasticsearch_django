# ��user_agent_list�� ��ÿ��requestʱ����user_agent_list�����ȡ��һ��
user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
]

headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': ""
    } 

import random  #���������
random_index = random.randint(0, len(user_agent_list)-1)
random_agent = user_agent_list[random_index]
headers["User-Agent"] = random_agent



# ͨ��downloadmiddleware�������user-agent












