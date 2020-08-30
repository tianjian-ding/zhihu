# 获取每个知乎热榜对应的所有回答
import requests
import json
import time
import pandas as pd

#
#
# def get_data(url, headers):
#     '''
#     功能：访问 url 的网页，获取网页内容并返回
#     参数：
#         url ：目标网页的 url
#     返回：目标网页的 html 内容
#     '''
#
#     try:
#         r = requests.get(url, headers=headers)
#         r.encoding = 'uft-8'
#         r.raise_for_status()
#         return r.text
#
#     except requests.HTTPError as e:
#         print(e)
#         print("HTTPError")
#     except requests.RequestException as e:
#         print(e)
#     except:
#         print("Unknown Error !")
#
#
# def parse_data(html):
#     '''
#     功能：提取 html 页面信息中的关键信息，并整合一个数组并返回
#     参数：html 根据 url 获取到的网页内容
#     返回：存储有 html 中提取出的关键信息的数组
#     '''
#     json_data = json.loads(html)['data']
#     comments = []
#     return json_data
#
#     try:
#         for item in json_data:
#             comment = []
#             comment.append(item['id'])  # answer id
#             comment.append(item['question']['id'])  # question id
#             comment.append(item['question']['title'])  # 问题题目
#             comment.append(item['question']['created'])  # 创建时间
#             comment.append(item['question']['updated_time'])  # 更新时间
#             comment.append(item['author']['name'])  # 姓名
#             comment.append(item['author']['gender'])  # 性别
#             comment.append(item['voteup_count'])  # 点赞数
#             comment.append(item['comment_count'])  # 评论数
#             comment.append(item['content'])  # 回答内容
#
#         return comments
#
#     except Exception as e:
#         print(comment)
#         print(e)
#
#
# def save_data(comments):
#     '''
#     功能：将comments中的信息输出到文件中/或数据库中。
#     参数：comments 将要保存的数据
#     '''
#     filename = './comments.csv'
#
#     dataframe = pd.DataFrame(comments)
#     dataframe.to_csv(filename, mode='a', index=False, sep=',', header=False)
#
#
# def main():
#     currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 标定当前时间
#
#     headers = {
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#     }
#
#     page = 0
#     question_id = '275359100'
#     url = 'https://www.zhihu.com/api/v4/questions/' + question_id + '/answers?include=data%\
#     5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2C\
#     annotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2C\
#     can_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2C\
#     created_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2C\
#     is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2C\
#     is_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2C\
#     badge%5B%2A%5D.topics&limit=5&offset=' + str(page) + '&platform=desktop&sort_by=default'
#
#     # get total cmts number
#     html = get_data(url, headers)
#     totals = json.loads(html)['paging']['totals']
#
#     print(totals)
#     print('---' * 10)
#
#     while (page < 10):
#         html = get_data(url, headers)
#         comments = parse_data(html)
#
#         save_data(comments)
#
#         print(f"\r{page}/{totals}", end="")
#         page += 5
#
#
# if __name__ == '__main__':
#     main()

# temp = "2020-08-30 00:44:28"
# questions_df = pd.read_csv('questions.csv', header=None)
# print(questions_df.head())
import MySQLdb