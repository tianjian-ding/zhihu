import requests
import json
import time
import re
import pandas as pd
from bs4 import BeautifulSoup
import MySQLdb

# 获取当前知乎热榜

# 获取当前知乎热榜

def get_hot_zhihu(url, headers):
    res = requests.get(url, headers=headers)
    content = BeautifulSoup(res.text, "html.parser")
    hot_data = content.find('script', id='js-initialData').string
    hot_json = json.loads(hot_data)
    hot_list = hot_json['initialState']['topstory']['hotList']
    return hot_list


def get_question_detail(question_id, headers):
    url = "https://www.zhihu.com/question/" + question_id
    res = requests.get(url, headers=headers)
    content = BeautifulSoup(res.text, "html.parser")
    content.html.body.div.div.main.find_all('meta')

    detail = []

    detail.append(content.main.find_all('meta')[2].get("content"))  # 关键词
    detail.append(content.main.find_all('meta')[4].get("content"))  # 评论数

    created_time = re.search(r'(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})',
                             content.main.find_all('meta')[5].get("content"))
    detail.append(created_time.group(1) + " " + created_time.group(2))  # 创建时间

    modified_time = re.search(r'(\d{4}-\d{2}-\d{2}).(\d{2}:\d{2}:\d{2})',
                              content.main.find_all('meta')[6].get("content"))
    detail.append(modified_time.group(1) + " " + modified_time.group(2))  # 最早修改时间

    detail.append("".join(re.findall('\d', content.find_all('strong')[0].string)))  # 关注人数
    detail.append("".join(re.findall('\d', content.find_all('strong')[1].string)))  # 浏览人数

    return detail


def parse_questions(hot_list, current_time, headers):
    questions = []

    for q in hot_list:
        question = []

        question.append(current_time)
        question.append(q['target']['titleArea']['text'])  # 问题内容
        question.append(str(q['feedSpecific']['answerCount']))  # 回答数
        question.append(re.search(r'\d*', q['target']['metricsArea']['text']).group(0))  # 热度 单位 万

        answer_id = re.search(r'https://www.zhihu.com/question/(\d*)', q['target']['link']['url']).group(1)
        question.append(answer_id)  # answer id

        detail = get_question_detail(answer_id, headers)

        question += detail

        questions.append(tuple(question))
    print("data generated")
    return questions


def save_questions(questions):
    print("start to insert")

    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='dtjdtj123',
        db='zhihu',
        charset="utf8"
    )

    cur = conn.cursor()
    sql = f"""INSERT INTO `zhihu`.`hotboard`
    (`recordId`,
    `currentTime`,
    `questionTitle`,
    `answersNumber`,
    `hotValue`,
    `answerId`,
    `keywords`,
    `commentsNumber`,
    `createdTime`,
    `modifiedTime`,
    `followersNumber`,
    `visitNumber`)
    VALUES
    (0,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """
    try:

        # 执行sql语句
        cur.executemany(sql, questions)  # 批量插入
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




def main():
    url = 'https://www.zhihu.com/billboard'
    headers = {"User-Agent": "'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                             "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 标定当前时间
    print(current_time)
    hot_list = get_hot_zhihu(url, headers)
    questions = parse_questions(hot_list, current_time, headers)

    save_questions(questions)


if __name__ == '__main__':
    main()

