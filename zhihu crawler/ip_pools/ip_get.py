import requests
import random
from lxml import etree
from fake_useragent import UserAgent


# 生成随机的User-Agent
def get_random_ua():
    # 创建User-Agent对象
    ua = UserAgent()
    # 随机生成1个User-Agent
    return ua.random

# IP访问测试网站: http://httpbin.org/get
url = 'http://httpbin.org/get'

#
# # 从西刺代理网站上获取随机的代理IP
# def get_ip_list():
#     headers = {'User-Agent': get_random_ua()}
#     # 访问西刺代理网站国内高匿代理，找到所有的tr节点对象
#     res = requests.get('https://www.xicidaili.com/nn/', headers=headers)
#     parse_html = etree.HTML(res.text)
#     # 基准xpath，匹配每个代理IP的节点对象列表
#     ipobj_list = parse_html.xpath('//tr')
#     # 定义空列表，获取网页中所有代理IP地址及端口号
#     ip_list = []
#     # 从列表中第2个元素开始遍历，因为第1个为: 字段名（国家、IP、... ...）
#     for ip in ipobj_list[1:]:
#         ip_info = ip.xpath('./td[2]/text()')[0]
#         port_info = ip.xpath('./td[3]/text()')[0]
#         ip_list.append(
#             {
#                 'http': 'http://' + ip_info + ':' + port_info,
#                 'https': 'https://' + ip_info + ':' + port_info
#             }
#         )
#     # 返回代理IP及代理池（列表ip_list）
#     return ip_list


# 主程序寻找测试可用代理
def main_print():
    # 获取抓取的所有代理IP
    with open("./http_ip.txt",'r') as ip_file:
        ip_list = ip_file.read().split("\n")

    # print(len(ip_list))
    # 将不能使用的代理删除
    for proxy_ip in ip_list:
        try:
            # 设置超时时间，如果代理不能使用则切换下一个
            headers = {'User-Agent': get_random_ua()}
            res = requests.get(url=url, headers=headers, proxies=proxy_ip, timeout=10)
            res.encoding = 'utf-8'
            print(res.text)

        except Exception as e:
            # 此代理IP不能使用，从代理池中移除
            ip_list.remove(proxy_ip)
            print('%s不能用，已经移除' % proxy_ip)
            # 继续循环获取最后1个代理IP
            continue

    # print(len(ip_list))
    #将可用代理保存到本地文件
    with open('proxies.txt','w') as f:
        for ip in ip_list:
            f.write(ip + '\n')

if __name__ == '__main__':
    main_print()