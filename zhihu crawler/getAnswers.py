# -*- coding: utf-8 -*-


# 获取每个知乎热榜对应的所有回答

import requests
import json
import time
import re
from bs4 import BeautifulSoup
import MySQLdb
import random



def random_ip():
    with open("./ip_pools/proxies.txt", 'r') as ip_file:
        ip_list = ip_file.read().split("\n")

    r = random.randint(0, len(ip_list))

    return {"http" : ip_list[r]}   # 随机抽取一个ip


def get_data(url, headers):
    '''
    功能：访问 url 的网页，获取网页内容并返回
    参数：
        url ：目标网页的 url
    返回：目标网页的 html 内容
    '''

    try:

        r = requests.get(url, headers=headers, proxies=random_ip())
        r.encoding = 'uft-8'
        r.raise_for_status()
        return r.text

    except requests.HTTPError as e:
        print(e)
        print("HTTPError")
    except requests.RequestException as e:
        print(e)
    except:
        print("Unknown Error !")


def parse_data(html, current_time):
    '''
    功能：提取 html 页面信息中的关键信息，并整合一个数组并返回
    参数：html 根据 url 获取到的网页内容
    返回：存储有 html 中提取出的关键信息的数组
    '''
    json_data = json.loads(html)['data']
    comments = []

    try:
        for item in json_data:
            comment = []

            comment.append(current_time) #执行时间
            comment.append(item['id'])  # answer id
            comment.append(item['question']['id'])  # question id
            # comment.append(item['question']['title'])  # 问题题目
            comment.append(item['question']['created'])  # 创建时间
            comment.append(item['question']['updated_time'])  # 更新时间
            comment.append(item['author']['name'])  # 姓名
            comment.append(item['author']['gender'])  # 性别
            comment.append(item['voteup_count'])  # 点赞数
            comment.append(item['comment_count'])  # 评论数
            comment.append(item['content'])  # 回答内容
            comments.append(tuple([str(i) for i in comment]))

        return comments

    except Exception as e:
        print("parse data error")
        print(e)


def get_question_id(current_time):
    print(current_time)
    # 打开数据库连接
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='dtjdtj123',
        db='zhihu',
        charset="utf8mb4"
    )

    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()

    # SQL 查询语句
    sql = "select questionId from zhihu.hotboard where currentTime = '%s';" %current_time

    results = ''

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()

    except Exception as e:
        print(f"Error: unable to fecth data, {e}")

    # 关闭数据库连接
    conn.close()

    return [i[0] for i in results]


def save_data(comments):
    '''
    功能：将comments中的信息输出到文件中/或数据库中。
    参数：comments 将要保存的数据
    '''
    print("start to insert")

    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='dtjdtj123',
        db='zhihu',
        charset="utf8mb4"
    )

    cur = conn.cursor()

    sql_answers = f""" INSERT INTO
    `zhihu`.`answers`
    (`recordId`,
     `currentTime`,
     `answerId`,
     `questionId`,
     `createdTime`,
     `updateTime`,
     `authorName`,
     `authorGender`,
     `voteUpNumber`,
     `commentsNumber`,
     )
        VALUES
        (0,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """

    sql_answers_content = f""" INSERT INTO
    `zhihu`.`answers_content`
    (
     `answerId`,
     `answerContent`
     )
        VALUES
        (0,%s,%s);
        """


    try:

        # 执行sql语句
        cur.executemany(sql_answers, [i[:9] for i in comments])  # 批量插入
        cur.executemany(sql_answers_content, [(i[1], i[9]) for i in comments])
        # 提交到数据库执行
        conn.commit()
        print("insert successful")
    except Exception as e:
        # Rollback in case there is any error
        print('insert error')
        print(e)
        conn.rollback()

    cur.close()
    conn.close()




def get_answers(question_id, current_time):


    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }

    page = 0

    url = f"""
        https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={page}&platform=desktop&sort_by=default
"""
    # get total cmts number
    html = get_data(url, headers)

    totals = json.loads(html)['paging']['totals']

    print(totals)
    print('---' * 10)


    comments = []

    while (page < totals):
        html = get_data(url, headers)
        comments += parse_data(html, current_time)
        print(f"\r{page}/{totals}", end="")
        page += 5

    save_data(comments)

def main(current_time):
    # currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 标定当前时间
    # current_time = '2020-08-30 01:44:08'
    question_list = get_question_id(current_time)
    id_number = len(question_list)
    count = 0
    for qid in question_list:
        print(qid)
        get_answers(qid, current_time)
        count+=1
        print(f"\ranswers of {count}/{id_number}st question collected", end="")


if __name__ == '__main__':
    main()

