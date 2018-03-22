#用于将新闻中的评论内容单独存表
# -*- coding:utf-8 -*-
import csv, re
import pandas
import sys
maxInt = sys.maxsize
decrement = True


def csv_process():
    # 初始化list用于存放对应数据
    id = []
    username = []
    date_time = []
    content = []
    news_id = []
    # 读取新闻csv
    news_dict = csv.reader(open('A:/Python/NewsSpider/scrapyspider/网易新闻0111_1.csv ', encoding='utf-8'))
    count = 0
    # 遍历csv中所有新闻
    for items in news_dict:
        try:
            newsid = items[5]
            comment_data = items[1]

            # 寻找每条评论起止
            keyword_start =u'{'
            keyword_end = u'}'
            comment_start = [m.start() for m in re.finditer(keyword_start, comment_data)]
            comment_end = [n.start() for n in re.finditer(keyword_end, comment_data)]

            # 提取每条评论
            for i in range(0,len(comment_end)):
                comments = comment_data[comment_start[i]:comment_end[i]]

                # 提取评论id
                id_start = comments.find("'id':")
                id_end = comments.find(", 'username'")
                id.append(comments[id_start + 5 : id_end])

                # 提取评论用户名
                username_start = comments.find("'username':")
                username_end = comments.find(", 'date_time'")
                username.append(comments[username_start + 13 : username_end-1])

                # 提取评论时间
                datetime_start = comments.find("'date_time':")
                datetime_end = comments.find(", 'content'")
                date_time.append(comments[datetime_start + 14 : datetime_end-1])

                # 提取评论内容
                content_start = comments.find("'content':")
                content_end = comments.find("}]")
                content.append(comments[content_start + 12: content_end])

                # 添加新闻id
                news_id.append(newsid)
            count += 1
        except:
            continue

    #格式化评论数据，字典中的key值即为csv中列名
    dataframe = pandas.DataFrame(
        {'id':id,
         'username':username,
         'date_time':date_time,
         'content':content,
         'news_id':news_id}
    )

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv(
        "A:/Python/NewsSpider/scrapyspider/网易新闻0111_1的评论.csv",
        index=False,
        encoding='utf_8_sig'
    )

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt / 10)
        decrement = True
csv_process()