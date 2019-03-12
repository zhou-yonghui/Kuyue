import pymysql
from django.shortcuts import HttpResponse, render, redirect,HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse
from qiniu import Auth, put_file, etag
import redis
import jieba
import json
import time
import random
import datetime

r = redis.Redis(host='139.196.136.63', port=6379)
conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)

dict1 = {'xuanhuan': '玄幻', 'qihuan': '奇幻', 'wuxia': '武侠', 'xianxia': '仙侠', 'dushi': '都市', 'xianshi': '现实',
         'junshi': '军事',
         'lishi': '历史', 'youxi': '游戏', 'tiyu': '体育', 'kehuan': '科幻', 'lingyi': '灵异', 'erciyuan': '二次元',
         'duanpian': '短片'}
dict2 = {'lianzai': '连载中', 'wanben': '完本'}
dict3 = {'free': [(-1), 0], 'fufei': [0, 1000]}
dict4 = {'w1': [0, 30 * 10 ** 4], 'w2': [30 * 10 ** 4, 50 * 10 ** 4], 'w3': [50 * 10 ** 4, 100 * 10 ** 4],
         'w4': [100 * 10 ** 4, 200 * 10 ** 4], 'w5': [200 * 10 ** 4, 6000 * 10 ** 4]}

dict5 = {'free': '免费', 'fufei': '付费'}
dict6 = {'w1': '30万字以下', 'w2': '30-50万字', 'w3': '50-100万字', 'w4': '100-200万字', 'w5': '200万字以上'}


def Header(request):
    try:
        userid = request.Session.get('user_id')
        conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from n_user where user_id='%s'" % (userid)
        cursor.execute(sql)
        user = cursor.fetchone()
        print(user)
        request.session['user_name'] = user['user_name']
        return render(request, 'Header.html')
    except:
        i = 1
        return render(request, 'Header.html')


def Details(request):
    book_id = request.GET.get("book_id")
    book_id = int(book_id)
    print(book_id)
    # 修改
    try:
        user_id = request.session['user_id']
        info = 'in'
    except:
        info = 'out'
    print('===================================')
    print(info)
    if info == 'in':
        cursor.execute("select book_id from n_buyrecord where user_id=%s", [user_id])
        books = cursor.fetchall()
        print(books)
        for row in books:
            print(type(row['book_id']))
            if row['book_id'] == int(book_id):
                info = 'true'

    print(info)
    cursor.execute("select * from n_bookinfo where book_id=%s", [book_id, ])
    novels_list = cursor.fetchone()
    print(novels_list)
    cursor.execute("select * from n_user where user_id=%s", [novels_list['user_id'], ])
    user_list = cursor.fetchone()
    print(user_list)
    cursor.execute("select * from n_kind where kind_id=%s", [novels_list['kind_id'], ])
    kind_list = cursor.fetchone()
    print(kind_list)
    print(user_list['user_id'])
    cursor.execute("select * from n_bookinfo where user_id=%s and book_id!=%s", [user_list['user_id'], book_id, ])
    others_novels = cursor.fetchall()
    print(others_novels)
    print(novels_list['kind_id'])
    cursor.execute("select * from n_bookinfo where kind_id=%s and book_id!=%s limit 4",
                   [novels_list['kind_id'], book_id, ])
    same_novels = cursor.fetchall()
    print(same_novels)
    cursor.execute(
        "select * from n_bookinfo join n_kind on n_bookinfo.kind_id=n_kind.kind_id  where n_bookinfo.kind_id=%s and book_id!=%s limit 8",
        [novels_list['kind_id'], book_id, ])
    same_novels_1 = cursor.fetchall()
    print(same_novels_1)
    cursor.execute("select chapter_id,chapter_name,book_id from n_chapter where book_id=%s", [book_id, ])
    chapter_list = cursor.fetchall()
    print(chapter_list)
    chapter_list1 = chapter_list[0]
    # 评论
    cursor.execute(
        "select * from n_talk join n_user on n_talk.user_id=n_user.user_id where n_talk.book_id=%s and parent_id IS NULL limit 5",
        [book_id, ])
    talk_list = cursor.fetchall()
    # 查获价格
    cursor.execute("select book_price from n_bookinfo where book_id=%s ", [book_id])
    rprice = cursor.fetchone()

    cursor.execute(
        "select * from n_bookinfo a,n_user b,n_kind c where a.user_id=b.user_id and a.kind_id=c.kind_id and book_id=%s",
        [book_id])
    bookmag = cursor.fetchone()
    print(talk_list)
    shujia = "加入书架"
    try:
        user_id = request.session['user_id']
        cursor.execute("select * from n_bookcase where book_id=%s and user_id=%s", [book_id, user_id, ])
        n_bookcase_list = cursor.fetchone()
        if n_bookcase_list == None:
            shujia = "加入书架"
        else:
            shujia = "已收藏"
    except:
        print("没登录")
    return render(request, 'Details.html',
                  {'novels_list': novels_list, 'user_list': user_list, 'kind_list': kind_list,
                   'others_novels': others_novels[0], 'same_novels': same_novels, 'chapter_list': chapter_list,
                   'talk_list': talk_list, 'same_novels_1': same_novels_1, 'chapter_list1': chapter_list1,
                   'shujia': shujia, 'rprice': rprice, 'bookmag': bookmag, 'info': info})


def toupiao(request):
    try:
        conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        user_id = request.session['user_id']
        data = request.POST
        print(user_id)
        print(data)
        cursor.execute("select user_votes from n_user where user_id=%s", [user_id, ])
        user_votes = cursor.fetchone()
        print(user_votes)
        counts = int(user_votes['user_votes'])
        if counts == 0:
            title = "推荐票不足请重新选择！"
            response = JsonResponse({"title": title})
            return response
        votecount = data['votecount'].strip()
        if votecount == "一张月票":
            count = 1
        elif votecount == "二张月票":
            count = 2
        elif votecount == "三张月票":
            count = 3
        elif votecount == "全部月票":
            count = int(user_votes['user_votes'])
        count1 = counts - count
        print(count1)
        if count1 >= 0:
            cursor.execute("update n_user set user_votes=%s where user_id=%s", [count1, user_id, ])
            conn.commit()
        if count1 < 0:
            title = "推荐票不足请重新选择！"
            response = JsonResponse({"title": title})
            return response
        else:
            print(data['book_id'])
            cursor.execute("select book_ticketcount from n_bookinfo where book_id=%s", [data['book_id'], ])
            book_ticketcount = cursor.fetchone()
            book_ticketcount = int(book_ticketcount['book_ticketcount'])
            cursor.execute("update n_bookinfo set book_ticketcount=%s where book_id=%s",
                           [count + book_ticketcount, data['book_id'], ])
            conn.commit()
            cursor.execute("select book_ticketcount from n_bookinfo where book_id=%s", [data['book_id'], ])
            book_ticketcount1 = cursor.fetchone()
            title = "恭喜投票成功！"
            response = JsonResponse({"title": title, "book_ticketcount": book_ticketcount1['book_ticketcount']})
            return response
    except:
        title = "请先登录！！！"
        response = JsonResponse({"title": title})
        return response


def shujia(request):
    try:
        user_id = request.session['user_id']
        print(user_id)
        data = request.POST
        cursor.execute("select * from n_bookcase where book_id=%s and user_id=%s", [data['book_id'], user_id, ])
        n_bookcase_list = cursor.fetchone()
        if n_bookcase_list != None:
            title = "请不要重复收藏！！！"
            response = JsonResponse({"title": title})
            return response
        cursor.execute("select max(bookcase_id) from n_bookcase")
        max_score_id = cursor.fetchone()
        print(max_score_id)
        if max_score_id['max(bookcase_id)'] == None:
            bookcase_id = 0
        else:
            bookcase_id = max_score_id['max(bookcase_id)']
        bookcase_id = bookcase_id + 1
        cursor.execute(
            "insert into n_bookcase(bookcase_id,book_id,user_id) values(%s,%s,%s)",
            [bookcase_id, data['book_id'], user_id, ])
        conn.commit()
        response = JsonResponse({"data": 1})
        return response
    except:
        title = "请先登录！！！"
        response = JsonResponse({"title": title})
        return response


def pingfen(request):
    title = ""
    try:
        user_id = request.session['user_id']
        print(user_id)
        data = request.POST
        index = data['index']
        print(index)
        if index == "":
            title = "请先评价！！！"
            response = JsonResponse({"title": title})
            return response
        cursor.execute("select * from n_scorerecord where book_id=%s and user_id=%s", [data['book_id'], user_id])
        lst = cursor.fetchone()
        if lst:
            title = "请不要重复评价！！！"
            response = JsonResponse({"title": title})
            return response
        title = "评分成功！！！"
        print(title)
        index = int(index) + 1
        score = index * 2
        cursor.execute("select book_estimate,book_estimatecount from n_bookinfo where book_id=%s", [data['book_id'], ])
        book_estimate = cursor.fetchone()
        print(book_estimate['book_estimate'])
        print(book_estimate['book_estimatecount'])
        book_estimate_1 = (book_estimate['book_estimate'] * book_estimate['book_estimatecount'] + score) / (
                book_estimate['book_estimatecount'] + 1)
        book_estimate_1 = '%.1f' % book_estimate_1
        cursor.execute("update n_bookinfo set book_estimate=%s where book_id=%s",
                       [book_estimate_1, data['book_id'], ])
        conn.commit()
        cursor.execute("select book_estimate from n_bookinfo where book_id=%s", [data['book_id'], ])
        book_estimate2 = cursor.fetchone()
        book_estimate3 = '%.1f' % (book_estimate2['book_estimate'])
        cursor.execute("select max(score_id) from n_scorerecord")
        max_score_id = cursor.fetchone()
        print(max_score_id['max(score_id)'] + 1)
        score_id = max_score_id['max(score_id)'] + 1
        cursor.execute(
            "insert into n_scorerecord(score_id,user_id,book_id,book_estimate) values(%s,%s,%s,%s)",
            [score_id, user_id, data['book_id'], score, ])
        conn.commit()
        cursor.execute("select book_estimatecount from n_bookinfo where book_id=%s", [data['book_id'], ])
        book_estimatecount = cursor.fetchone()
        book_estimatecount = int(book_estimatecount['book_estimatecount']) + 1
        cursor.execute("update n_bookinfo set book_estimatecount=%s where book_id=%s",
                       [book_estimatecount, data['book_id'], ])
        conn.commit()
        response = JsonResponse(
            {"title": title, "book_estimatecount": book_estimatecount, "book_estimate": book_estimate3})
        return response
    except:
        title = "请先登录！！！"
        response = JsonResponse({"title": title})
        return response


def Talk(request):
    if request.method == "GET":
        book_id = request.GET.get("book_id")
        cursor.execute("select * from n_bookinfo where book_id=%s", [book_id, ])
        novels_list = cursor.fetchone()
        print(novels_list)
        cursor.execute("select * from n_user where user_id=%s", [novels_list['user_id'], ])
        user_list = cursor.fetchone()
        print(user_list)
        cursor.execute(
            "select * from n_talk join n_user on n_talk.user_id=n_user.user_id where n_talk.book_id=%s and parent_id IS NULL",
            [book_id, ])
        talk_list = cursor.fetchall()
        print(len(talk_list))
        return render(request, 'Talk.html',
                      {'novels_list': novels_list, 'user_list': user_list, 'talk_list': talk_list,
                       'len_talk_list': len(talk_list)})
    else:
        try:
            user_id = request.session['user_id']
            time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(time_now)
            data = request.POST
            cursor.execute("select max(talk_id) from n_talk ")
            max_talk_id = cursor.fetchone()
            max_talk_id = max_talk_id['max(talk_id)'] + 1
            cursor.execute(
                "insert into n_talk(talk_id,talk_content,talk_time,talk_like,response_count,book_id,user_id) values(%s,%s,%s,%s,%s,%s,%s)",
                [max_talk_id, data['html'], time_now, 0, 0, data['book_id'], user_id, ])
            conn.commit()
            cursor.execute(
                "select * from n_talk join n_user on n_talk.user_id=n_user.user_id where n_talk.book_id=%s and parent_id IS NULL",
                data['book_id'])
            talk_list = cursor.fetchall()
            print(talk_list)
            len_talk_list = len(talk_list)
            print(len_talk_list)
            response = JsonResponse({"data": talk_list, "len_talk_list": len_talk_list})
            return response
        except:
            title = "请先登录！！！"
            response = JsonResponse({"title": title})
            return response


def TalkDetails(request):
    if request.method == "GET":
        talk_id1 = request.GET.get("talk_id")
        print(talk_id1)
        cursor.execute("select * from n_talk join n_bookinfo on n_talk.book_id=n_bookinfo.book_id where talk_id=%s",
                       [talk_id1, ])
        book_list = cursor.fetchone()
        print(book_list)
        cursor.execute("select * from n_talk join n_user on n_talk.user_id=n_user.user_id where talk_id=%s",
                       [talk_id1, ])
        talk_list_1 = cursor.fetchone()
        print(talk_list_1)
        cursor.execute("select * from n_talk where book_id=%s", [book_list['book_id']])
        talk_list = cursor.fetchall()
        print(talk_list)
        for i in talk_list:
            i['children_contents'] = []
        print(talk_list)
        comment_dict = {}
        for d in talk_list:
            talk_id = d.get('talk_id')
            comment_dict[talk_id] = d
        print(comment_dict)
        for k in comment_dict:
            parent_id = comment_dict[k]['parent_id']
            if parent_id:
                comment_dict[parent_id]['children_contents'].append(comment_dict[k])
        print(comment_dict)
        res_list = []
        for i in comment_dict:
            if not comment_dict[i]['parent_id']:
                res_list.append(comment_dict[i])
        print(res_list[0])
        print('+++++++++++++++++++++++')
        print(talk_id1)
        lst1 = []
        for j in res_list:
            print(j)
            if int(j['talk_id']) == int(talk_id1):
                print(1)
                lst1.append(j)
        print(lst1)
        print('+++++++++++++++++++++++')

        print(lst1)
        global lst
        lst = []
        response = get_content(lst1)
        response1 = sorted(response, key=lambda x: int(x['talk_id']))
        print(response1)
        k = 1
        for i in response1:
            i['floor_id'] = k
            k += 1
        return render(request, 'TalkDetails.html',
                      {'talk_list_1': talk_list_1, 'response': response1, 'book_list': book_list})
    else:
        try:
            user_id = request.session['user_id']
            time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print(time_now)
            data = request.POST
            print(data['talk_id'])
            cursor.execute("select max(talk_id) from n_talk ")
            max_talk_id = cursor.fetchone()
            max_talk_id = max_talk_id['max(talk_id)'] + 1
            print(max_talk_id)
            cursor.execute(
                "insert into n_talk(talk_id,talk_content,talk_time,talk_like,response_count,book_id,user_id,parent_id) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                [max_talk_id, data['html'], time_now, 0, 0, data['book_id'], user_id, data['talk_id'], ])
            conn.commit()
            cursor.execute("select * from n_talk where talk_id=%s", [max_talk_id, ])
            user_talk = cursor.fetchone()
            print(add_response(user_talk))
            print(user_talk)
            print(data['talk_id'])
            print(data['book_id'])
            print(data['html'])
            cursor.execute("select * from n_talk where book_id=%s", [data['book_id']])
            talk_list = cursor.fetchall()
            print(talk_list)
            for i in talk_list:
                i['children_contents'] = []
            print(talk_list)
            comment_dict = {}
            for d in talk_list:
                talk_id = d.get('talk_id')
                comment_dict[talk_id] = d
            print(comment_dict)
            for k in comment_dict:
                parent_id = comment_dict[k]['parent_id']
                if parent_id:
                    comment_dict[parent_id]['children_contents'].append(comment_dict[k])
            print(comment_dict)
            res_list = []
            for i in comment_dict:
                if not comment_dict[i]['parent_id']:
                    res_list.append(comment_dict[i])
            print("+++++++++++++++++++++")
            print(data['talk_id'])
            cursor.execute("select * from n_talk where talk_id=%s", [data['talk_id'], ])
            talk_chid = cursor.fetchone()
            print("+++++++++++++++++")
            abc = find(talk_chid)
            # print(talk_id)
            lst1 = []
            for j in res_list:
                print(j)
                if int(j['talk_id']) == abc:
                    lst1.append(j)
            print(lst1)
            print("+++++++++++++++")
            lst = []
            response = get_content(lst1)
            response1 = sorted(response, key=lambda x: int(x['talk_id']))
            print(response1)
            k = 1
            for i in response1:
                i['floor_id'] = str(k)
                k += 1
            response = JsonResponse({"data": response1})
            return response
        except:
            title = "请先登录！！！"
            response = JsonResponse({"title": title})
            return response


def find(talk_chid):
    abc = talk_chid['talk_id']
    if talk_chid['parent_id']:
        cursor.execute("select * from n_talk where talk_id=%s", [talk_chid['parent_id'], ])
        talk_parent = cursor.fetchone()
        abc = find(talk_parent)
        return abc
    else:
        return abc


def add_response(user_talk):
    if user_talk['parent_id']:
        cursor.execute("select * from n_talk where talk_id=%s", [user_talk['parent_id'], ])
        user_parent = cursor.fetchone()
        cursor.execute("update n_talk set response_count=%s where talk_id=%s",
                       [user_parent['response_count'] + 1, user_parent['talk_id']])
        conn.commit()
        if user_parent['parent_id']:
            add_response(user_parent)
    return 1


def get_content(lst1):
    for i in lst1:
        if i['parent_id']:
            dict = {}
            cursor.execute("select * from n_talk where talk_id=%s", [i['parent_id'], ])
            user_parent = cursor.fetchone()
            cursor.execute("select * from n_user where user_id=%s", [user_parent['user_id'], ])
            user_parent1 = cursor.fetchone()
            cursor.execute("select * from n_user where user_id=%s", [i['user_id'], ])
            user_child = cursor.fetchone()
            dict['talk_id'] = str(i['talk_id'])
            dict['user_id'] = str(user_child['user_id'])
            dict['user_name'] = user_child['user_name']
            dict['parent_name'] = user_parent1['user_name']
            dict['talk_content'] = i['talk_content']
            dict['response_count'] = str(i['response_count'])
            dict['talk_like'] = str(i['talk_like'])
            dict['talk_time'] = str(i['talk_time'])
            dict['user_image'] = user_child['user_image']
            lst.append(dict)
        if i['children_contents']:
            get_content(i['children_contents'])
    return lst


def Likes1(request):
    try:
        user_id = request.session['user_id']
        data = request.POST
        print(type(data['talk_id']))
        cursor.execute("select * from n_talk where talk_id=%s", [data['talk_id'], ])
        talk_1 = cursor.fetchone()
        print(talk_1['talk_like'])
        talk_like = talk_1['talk_like'] + 1
        cursor.execute("update n_talk set talk_like=%s where talk_id=%s",
                       [talk_like, data['talk_id'], ])
        conn.commit()
        response = JsonResponse({"talk_like": talk_like, 'response_count': talk_1['response_count']})
        return response
    except:
        title = "请先登录！！！"
        response = JsonResponse({"title": title})
        return response


def Likes2(request):
    try:
        user_id = request.session['user_id']
        data = request.POST
        print(type(data['talk_id']))
        cursor.execute("select * from n_talk where talk_id=%s", [data['talk_id'], ])
        talk_1 = cursor.fetchone()
        print(talk_1['talk_like'])
        talk_like = talk_1['talk_like'] - 1
        cursor.execute("update n_talk set talk_like=%s where talk_id=%s",
                       [talk_like, data['talk_id'], ])
        conn.commit()
        response = JsonResponse({"talk_like": talk_like, 'response_count': talk_1['response_count']})
        return response
    except:
        title = "请先登录！！！"
        response = JsonResponse({"title": title})
        return response


def MyTalk(request):
    user_id = request.GET.get("user_id")
    cursor.execute(
        "select * from n_talk join n_user on n_talk.user_id=n_user.user_id where n_talk.user_id=%s and parent_id IS NULL",
        [user_id, ])
    talk_list = cursor.fetchall()
    cursor.execute(
        "select * from n_talk join n_user on n_talk.user_id=n_user.user_id where parent_id=%s",
        [user_id, ])
    talk_list1 = cursor.fetchall()
    return render(request, 'MyTalk.html', {'talk_list': talk_list, 'talk_list1': talk_list1})


def Read(request):
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    chapter_id = request.GET.get("chapter_id")
    book_id = request.GET.get("book_id")

    # xiugai
    info = ''
    try:
        user_id = request.session['user_id']
        info = 'in'
    except:
        info = 'out'

    print(info)
    if info == 'in':
        cursor.execute("insert into n_readrecord (book_id,chapter_id,read_time,user_id)values(%s,%s,%s,%s)",
                       [book_id, chapter_id, nowTime, user_id])
        conn.commit()

    print(chapter_id)
    print(book_id)
    if chapter_id == None:
        chapter_id = 1
    cursor.execute("select * from n_chapter where chapter_id=%s and book_id=%s", [chapter_id, book_id])
    chapter = cursor.fetchall()
    print(chapter)
    cursor.execute("select chapter_id,chapter_name,book_id from n_chapter where book_id=%s", [book_id, ])
    chapter_list = cursor.fetchall()
    print(chapter_list)
    chapter_list1 = chapter_list[0]
    return render(request, 'Read.html',
                  {'chapter': chapter[0], 'chapter_list': chapter_list, 'chapter_list1': chapter_list1}, )

def Write_book(request):
    return render(request,'Write_book.html')

# 马荣
def main(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'select book_id,book_name,book_ticketcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id   order by book_ticketcount desc'
    cursor.execute(sql)
    tc = cursor.fetchall()
    tc_1 = tc[0]
    tc = tc[1:10]
    # print(tc)
    sql = 'select book_id,book_name,book_sellcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_sellcount desc'
    cursor.execute(sql)
    sc = cursor.fetchall()
    sc_1 = sc[0]
    sc = sc[1:10]
    sql = 'select book_id,book_name,book_words,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_words desc'
    cursor.execute(sql)
    bw = cursor.fetchall()
    bw_1 = bw[0]
    bw = bw[1:10]
    sql = 'select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_clickcount desc'
    cursor.execute(sql)
    cc = cursor.fetchall()
    cc_1 = cc[0]
    cc = cc[1:10]
    sql = 'select book_id,book_name,user_name from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_estimate desc'
    cursor.execute(sql)
    be = cursor.fetchall()
    be = be[0:10]
    sql = 'select book_id,book_name,book_estimatecount,book_introduction from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_estimatecount desc'
    cursor.execute(sql)
    ec = cursor.fetchall()
    ec1 = ec[0:3]
    ec2 = ec[3:6]
    ec3 = ec[6:9]
    i = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10']
    for i in ec:
        # i['book_introduction']=i['book_introduction'][0:30]

        i['book_introduction'] = i['book_introduction'].strip()[0:30].replace(' ', '').replace('\n', '').replace('\t',
                                                                                                                 '').replace(
            '\r', '')
    return render(request, 'main.html',
                  {'tc_1': tc_1, 'tc': tc, 'sc_1': sc_1, 'sc': sc, 'bw_1': bw_1, 'bw': bw, 'cc_1': cc_1, 'cc': cc,
                   'be': be, 'ec1': ec1, 'i': i, 'ec2': ec2, 'ec3': ec3})
    i = 1
    return render(request, 'main.html', {'i': 1})

def main2(request):
    i = 1
    return render(request, 'main.html', {'i': 1})


def ranking(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = 'select book_id,book_name,book_ticketcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id   order by book_ticketcount desc'
    cursor.execute(sql)
    tc = cursor.fetchall()
    tc_1 = tc[0]
    tc = tc[1:10]
    # print(tc)
    sql = 'select book_id,book_name,book_sellcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_sellcount desc'
    cursor.execute(sql)
    sc = cursor.fetchall()
    sc_1 = sc[0]
    sc = sc[1:10]
    sql = 'select book_id,book_name,book_words,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_words desc'
    cursor.execute(sql)
    bw = cursor.fetchall()
    bw_1 = bw[0]
    bw = bw[1:10]
    sql = 'select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_clickcount desc'
    cursor.execute(sql)
    cc = cursor.fetchall()
    cc_1 = cc[0]
    cc = cc[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '玄幻')
    cursor.execute(sql)
    xuanhuan = cursor.fetchall()
    xuanhuan_1 = xuanhuan[0]
    xuanhuan = xuanhuan[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '二次元')
    cursor.execute(sql)
    erciyuan = cursor.fetchall()
    erciyuan_1 = erciyuan[0]
    erciyuan = erciyuan[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '武侠')
    cursor.execute(sql)
    wuxia = cursor.fetchall()
    wuxia_1 = wuxia[0]
    wuxia = wuxia[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '仙侠')
    cursor.execute(sql)
    xianxia = cursor.fetchall()
    xianxia_1 = xianxia[0]
    xianxia = xianxia[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '都市')
    cursor.execute(sql)
    dushi = cursor.fetchall()
    dushi_1 = dushi[0]
    dushi = dushi[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '现实')
    cursor.execute(sql)
    xianshi = cursor.fetchall()
    xianshi_1 = xianshi[0]
    xianshi = xianshi[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '军事')
    cursor.execute(sql)
    junshi = cursor.fetchall()
    junshi_1 = junshi[0]
    junshi = junshi[1:10]
    sql = "select book_id,book_name,book_clickcount,kind_name,n_user.user_id,user_name,book_image from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
        '历史')
    cursor.execute(sql)
    lishi = cursor.fetchall()
    lishi_1 = lishi[0]
    lishi = lishi[1:10]
    return render(request, 'ranking list.html',
                  {'cc_1': cc_1, 'tc_1': tc_1, 'bw_1': bw_1, 'sc_1': sc_1, 'cc': cc, 'tc': tc, 'bw': bw, 'sc': sc,
                   'xuanhuan_1': xuanhuan_1, 'xuanhuan': xuanhuan, 'erciyuan': erciyuan, 'erciyuan_1': erciyuan_1,
                   'wuxia_1': wuxia_1, 'wuxia': wuxia, 'xianxia': xianxia, 'xianxia_1': xianxia_1, 'dushi_1': dushi_1,
                   'dushi': dushi, 'xianshi_1': xianshi_1, 'xianshi': xianshi, 'junshi_1': junshi_1, 'junshi': junshi,
                   'lishi_1': lishi_1, 'lishi': lishi})


def ranking_click(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method == 'POST':
            sid = request.POST.get('sid')
            kind = request.POST.get('kind')
            number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
            for i in sid:
                if i not in number:
                    sid = '1'
                    break
            # print(sid)
            sid = int(sid)
            list1 = []
            if kind is None or kind == 'None':
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_clickcount desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
                    kind)
            cursor.execute(sql)
            result = cursor.fetchall()
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid < 1:
                sid = 1
            elif sid > len(list1):
                sid = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            # print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            return render(request, 'ranking_click.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
        elif request.method == 'GET':
            sid = request.GET.get('sid')
            kind = request.GET.get('kind')
            a = sid.split(',')
            sid = int(a[0])
            b = a[1].split('=')
            snum = int(b[1])
            # print(sid,snum)
            sid = sid + snum
            sid = int(sid)
            list1 = []
            if kind is None or kind == 'None':
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_clickcount desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_clickcount desc" % (
                    kind)
            cursor.execute(sql)
            result = cursor.fetchall()
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            # print(result)
            return render(request, 'ranking_click.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
    except:
        sid = 1
        list1 = []
        sql = 'select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_clickcount desc'
        cursor.execute(sql)
        result = cursor.fetchall()
        alllen = len(result)
        if len(result) % 5 == 0:
            length = len(result) // 5
        else:
            length = len(result) // 5 + 1
        for x in range(1, length + 1):
            {
                list1.append(x)
            }
        # print(list1)
        a = 5 * (sid - 1)
        b = 5 * sid
        # print(a,b)
        result = result[a:b]
        # print(result)
        z = 1
        m = 1
        n = len(list1)
        list1 = list1[0:3]
        return render(request, 'ranking_click.html',
                      {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'z': z, 'm': m, 'n': n,
                       'kind': kind})


def ranking_ticket(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method == 'POST':
            sid = request.POST.get('sid')
            kind = request.POST.get('kind')
            print(kind, sid)
            number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
            if sid is None or sid == 'None':
                sid = '1'
            else:
                for i in sid:
                    if i not in number:
                        sid = '1'
                        break
            sid = int(sid)
            print(sid)
            list1 = []
            if kind is None or kind == 'None':
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_ticketcount desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_ticketcount desc" % (
                    kind)
            cursor.execute(sql)
            result = cursor.fetchall()
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid < 1:
                sid = 1
            elif sid > len(list1):
                sid = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            # print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            return render(request, 'ranking_ticket.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
        elif request.method == 'GET':
            sid = request.GET.get('sid')
            kind = request.GET.get('kind')
            a = sid.split(',')
            sid = int(a[0])
            b = a[1].split('=')
            snum = int(b[1])
            # print(sid,snum)
            sid = sid + snum
            sid = int(sid)
            list1 = []
            if kind is None or kind == 'None':
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_ticketcount desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_ticketcount desc" % (
                    kind)
            cursor.execute(sql)
            result = cursor.fetchall()
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            # print(result)
            return render(request, 'ranking_ticket.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
    except:
        sid = 1
        list1 = []
        sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_ticketcount desc"
        cursor.execute(sql)
        result = cursor.fetchall()
        alllen = len(result)
        if len(result) % 5 == 0:
            length = len(result) // 5
        else:
            length = len(result) // 5 + 1
        for x in range(1, length + 1):
            {
                list1.append(x)
            }
        # print(list1)
        a = 5 * (sid - 1)
        b = 5 * sid
        # print(a,b)
        result = result[a:b]
        # print(result)
        z = 1
        m = 1
        n = len(list1)
        list1 = list1[0:3]
        return render(request, 'ranking_ticket.html',
                      {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'z': z, 'm': m, 'n': n,
                       'kind': kind})


def ranking_sell(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method == 'POST':
            sid = request.POST.get('sid')
            kind = request.POST.get('kind')
            number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
            for i in sid:
                if i not in number:
                    sid = '1'
                    break
            sid = int(sid)
            # print(sid)
            list1 = []
            if kind is None or kind == 'None':
                kind == 'None'
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_sellcount desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_sellcount desc" % (
                    kind)
            cursor.execute(sql)
            result = cursor.fetchall()
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid < 1:
                sid = 1
            elif sid > len(list1):
                sid = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            # print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            return render(request, 'ranking_sell.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
        elif request.method == 'GET':
            sid = request.GET.get('sid')
            kind = request.GET.get('kind')
            # print(kind)
            # print(sid, kind)
            a = sid.split(',')
            sid = int(a[0])
            b = a[1].split('=')
            snum = int(b[1])
            # print(sid,snum)
            sid = sid + snum
            sid = int(sid)
            list1 = []
            if kind is None or kind == 'None':
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_sellcount desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_sellcount desc" % (
                    kind)
            # sql=sql+"AND"+'n_kind.kind_name'+"='"+kind+"'"+"order by book_sellcount desc"
            cursor.execute(sql)
            result = cursor.fetchall()
            # print(result)
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            # print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            # print(result)
            return render(request, 'ranking_sell.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
    except:
        sid = 1
        list1 = []
        sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_sellcount desc"
        cursor.execute(sql)
        result = cursor.fetchall()
        alllen = len(result)
        if len(result) % 5 == 0:
            length = len(result) // 5
        else:
            length = len(result) // 5 + 1
        for x in range(1, length + 1):
            {
                list1.append(x)
            }
        # print(list1)
        a = 5 * (sid - 1)
        b = 5 * sid
        # print(a,b)
        result = result[a:b]
        # print(result)
        z = 1
        m = 1
        n = len(list1)
        list1 = list1[0:3]
        return render(request, 'ranking_sell.html',
                      {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'z': z, 'm': m, 'n': n,
                       'kind': kind})


def ranking_len(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        if request.method == 'POST':
            sid = request.POST.get('sid')
            kind = request.POST.get('kind')
            number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
            for i in sid:
                if i not in number:
                    sid = '1'
                    break
            sid = int(sid)
            # print(sid)
            list1 = []
            if kind is None or kind == 'None':
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_words desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_words desc" % (
                    kind)
            cursor.execute(sql)
            result = cursor.fetchall()
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid < 1:
                sid = 1
            elif sid > len(list1):
                sid = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            # print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            return render(request, 'ranking_len.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
        elif request.method == 'GET':
            sid = request.GET.get('sid')
            kind = request.GET.get('kind')
            a = sid.split(',')
            sid = int(a[0])
            b = a[1].split('=')
            snum = int(b[1])
            # print(sid,snum)
            sid = sid + snum
            sid = int(sid)
            list1 = []
            if kind is None or kind == 'None':
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_words desc"
            else:
                sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id and n_kind.kind_name='%s' order by book_words desc" % (
                    kind)
            cursor.execute(sql)
            result = cursor.fetchall()
            alllen = len(result)
            if len(result) % 5 == 0:
                length = len(result) // 5
            else:
                length = len(result) // 5 + 1
            # print(length)
            for x in range(1, length + 1):
                {
                    list1.append(x)
                }
            z = 1
            m = 1
            n = len(list1)
            if sid - 2 > 1 and sid + 2 < len(list1):
                z = 3
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 == 1 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 > 1 and sid + 2 == len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            elif sid - 2 <= 0 and sid + 2 < len(list1):
                z = 1
                m = 1
                n = len(list1)
                list1 = list1[0:sid + 2]
            elif sid - 2 > 1 and sid + 2 > len(list1):
                z = 2
                m = 1
                n = len(list1)
                list1 = list1[sid - 3:sid + 2]
            print(list1)
            a = 5 * (sid - 1)
            b = 5 * sid
            # print(a, b)
            result = result[a:b]
            # print(result)
            return render(request, 'ranking_len.html',
                          {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'length': length, 'z': z,
                           'm': m, 'n': n, 'kind': kind})
    except:
        sid = 1
        list1 = []
        sql = "select * from n_bookinfo,n_kind,n_user where n_bookinfo.kind_id=n_kind.kind_id and n_bookinfo.user_id = n_user.user_id order by book_words desc"
        cursor.execute(sql)
        result = cursor.fetchall()
        alllen = len(result)
        if len(result) % 5 == 0:
            length = len(result) // 5
        else:
            length = len(result) // 5 + 1
        for x in range(1, length + 1):
            {
                list1.append(x)
            }
        # print(list1)
        a = 5 * (sid - 1)
        b = 5 * sid
        # print(a,b)
        result = result[a:b]
        # print(result)
        z = 1
        m = 1
        n = len(list1)
        list1 = list1[0:3]
        return render(request, 'ranking_len.html',
                      {'alllen': alllen, 'result': result, 'list1': list1, 'sid': sid, 'z': z, 'm': m, 'n': n,
                       'kind': kind})


def self(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    try:
        user = request.session.get('user_id')
        if user ==None:
            return render(request, 'login.html')
    except:
        return render(request, 'login.html')
    # print(user)
    sql = "select * from n_useraccount,n_user where n_user.user_id=n_useraccount.user_id and n_user.user_id='%s'" % (
        user)
    cursor.execute(sql)
    userinfo = cursor.fetchone()
    # print(userinfo)
    cursor.execute(
        "select * from n_bookcase join n_bookinfo on n_bookcase.book_id=n_bookinfo.book_id where n_bookcase.user_id=%s",
        [user, ])
    book_list = cursor.fetchall()
    # print(book_list)
    # userid=userinfo[0]['user_id']
    # sql="select * from n_bookcase,n_bookinfo where n_bookinfo.book_id = n_bookcase.book_id and n_bookcase.user_id='%s'"%(userid)
    # cursor.execute(sql)
    # bookinfo=cursor.fetchall()
    return render(request, 'self.html', {'user': userinfo, 'book_list': book_list})


def selfset(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == "GET":
        try:
            user = request.session.get('user_id')
            if user == None:
                return render(request, 'login.html')
        except:
            return render(request, 'login.html')
        if request.is_ajax():
            text = request.GET.get('text')
            sql = "update n_user set user_introduction ='%s' where user_id='%s'" % (text, user)
            cursor.execute(sql)
            conn.commit()
            # print(text,user)
        sql = "select * from n_useraccount,n_user where n_user.user_id=n_useraccount.user_id and n_user.user_id='%s'" % (
            user)
        cursor.execute(sql)
        userinfo = cursor.fetchone()
        # print(userinfo['user_introduction'])
        # print(userinfo['user_birth'])
        s = userinfo['user_address'].split('-')
        # print(s)
        address = {'province': s[0], 'city': s[1], 'area': s[2]}
        return render(request, 'selfset.html', {'user': userinfo, 'address': address, 'a': 1})
    else:
        user = request.session.get('user_id')
        if user == None:
            return render(request, 'login.html')
        username = request.POST.get('nickname')
        sex = request.POST.get('sex')
        date = request.POST.get('date')
        city = request.POST.get('city')
        province = request.POST.get('province')
        area = request.POST.get('district')
        try:
            # print('________')
            File = request.FILES.get("img")
            # print(File)
            with open('media/upload/img/' + File.name, 'wb')as f:  # with open 无法创建文件夹，需要自己创建
                for chunk in File.chunks():
                    f.write(chunk)
            access_key = 'kWMzCb6yGVJllsSSiYShDXZ3AIRyJ3T0FLAB96hF'
            secret_key = 'EOYODZJ8zPfG5UfRU3ddlA1h9iU9N5lJAqKQaFoi'
            q = Auth(access_key, secret_key)
            bucket_name = 'kuyue'
            key = File.name
            localfile = r"media/upload/img/" + File.name
            token = q.upload_token(bucket_name, key)
            ret, info = put_file(token, key, localfile)
            src = 'http://phd9lbnhk.bkt.clouddn.com/' + File.name
            cursor.execute("update n_user set user_image=%s where user_id=%s", [src, user])
            conn.commit()
        except:
            i = 1
        # print(File)
        sql = "select * from n_bookinfo,n_bookcase where n_bookinfo.book_id=n_bookcase.book_id and n_bookcase.user_id='%s'" % (
            user)
        cursor.execute(sql)
        book_list = cursor.fetchall()
        # print(type(city),province,area)
        sql = "update n_user set user_birth='%s' where user_id='%s'" % (date, user)
        cursor.execute(sql)
        conn.commit()
        sql = "update n_user set user_name='%s' where user_id='%s'" % (username, user)
        cursor.execute(sql)
        conn.commit()
        sql = "update n_user set user_sex='%s' where user_id='%s'" % (sex, user)
        cursor.execute(sql)
        conn.commit()
        try:
            province = int(province)
            sql = "select * from n_province where code='%s'" % (province)
            cursor.execute(sql)
            province = cursor.fetchone()
            province = province['name']
            sql = "select * from n_city where code='%s'" % (city)
            cursor.execute(sql)
            city = cursor.fetchone()
            city = city['name']
            sql = "select * from n_area where code='%s'" % (area)
            cursor.execute(sql)
            area = cursor.fetchone()
            area = area['name']
            address = province + '-' + city + '-' + area
            # print(address)
            sql = "update n_user set user_address='%s' where user_id='%s'" % (address, user)
            cursor.execute(sql)
            conn.commit()
            # print(nickname, nameid, sex_dict[sex], date, city, province, district)
        except:
            address = province + '-' + city + '-' + area
            # print(address)
            sql = "update n_user set user_address='%s' where user_id='%s'" % (address, user)
            cursor.execute(sql)
            conn.commit()
            # print(nickname, nameid, sex_dict[sex], date, city, province, district)
        sql = "select * from n_useraccount,n_user where n_user.user_id=n_useraccount.user_id and n_useraccount.user_id='%s'" % (
            user)
        cursor.execute(sql)
        userinfo = cursor.fetchone()
        print(book_list)
        request.session['user_name'] = userinfo['user_name']
        return render(request, 'self.html', {'user': userinfo, 'book_list': book_list})


# File = request.FILES.get("img")
# with open('media/upload/img/' + File.name, 'wb')as f:  # with open 无法创建文件夹，需要自己创建
#     for chunk in File.chunks():
#         f.write(chunk)
# access_key = 'O4uhB24lIhk5B_VR1Tj6IQ1pF0kKA18aIpEzs3Kv'
# secret_key = 'aEEnRGPsAGIRZCobHxBuRmao0Z3wQfi7NyQxzZJV'
# q = Auth(access_key, secret_key)
# bucket_name = 'tupian'
# key = File.name
# localfile = r"media/upload/img/" + File.name
# token = q.upload_token(bucket_name, key)
# ret, info = put_file(token, key, localfile)
# src = 'http://files.g4.xmgc360.com/' + File.name
# cursor.execute("update n_user set user_image=%s where user_id=%s", [src, 1])
# conn.commit()
# return render(request, 'self.html', {'src': src})


def getProvince(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select * from n_province "
    cursor.execute(sql)
    provinces = cursor.fetchall()
    res = []
    for i in provinces:
        res.append([i['code'], i['name']])
    return JsonResponse({'provinces': res})


def getCity(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    city_id = request.GET.get('city_id')
    sql = "select * from n_city where provincecode='%s'" % (city_id)
    cursor.execute(sql)
    cities = cursor.fetchall()
    res = []
    for i in cities:
        res.append([i['code'], i['name']])
    return JsonResponse({'cities': res})


def getDistrict(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    district_id = request.GET.get('district_id')
    sql = "select * from n_area where citycode='%s'" % (district_id)
    cursor.execute(sql)
    citys = cursor.fetchall()
    res = []
    for i in citys:
        res.append([i['code'], i['name']])
    return JsonResponse({'district': res})


# 周磊


def classify(request):
    type = request.GET.get('type')
    state = request.GET.get('state')
    shuxing = request.GET.get('shuxing')
    word = request.GET.get('word')

    sql = 'select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id '
    if type == None and state == None and shuxing == None and word == None:
        sql = 'select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id '
    else:
        if (type != 'None' and type != 'all'):
            sql = sql + " AND " + 'kind_name' + " = '" + dict1[type] + "'"
        if (state != 'None' and state != 'all' and state != ''):
            sql = sql + " AND " + 'a.book_state' + " = '" + dict2[state] + "'"
        if (shuxing != 'None' and shuxing != 'all' and shuxing != ''):
            sql = sql + " AND " + 'a.book_price' + " between '" + str(dict3[shuxing][0]) + "'AND'" + str(
                dict3[shuxing][1]) + "'"
        if (word != 'None' and word != 'all' and word != ''):
            sql = sql + " AND " + "a.book_words" + " between '" + str(dict4[word][0]) + "'AND'" + str(
                dict4[word][1]) + "'"

    print(sql)
    cursor.execute(sql)
    Contacts = cursor.fetchall()
    random.shuffle(Contacts)
    paginator = Paginator(Contacts, 12)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    try:
        page1 = int(request.GET.get('page'))
    except:
        page1 = None

    if page1 != None:
        page = page1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except (EmptyPage):
        contacts = paginator.page(paginator.num_pages)
    index = contacts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index - 2 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'classify.html',
                  {'type': type, 'state': state, 'shuxing': shuxing, 'word': word, 'contacts': contacts,
                   'page_range': page_range, 'start_index': start_index, 'end_index': end_index, 'dict1': dict1,
                   'dict2': dict2, 'dict5': dict5, 'dict6': dict6})


def row(request):
    type = request.GET.get('type')
    state = request.GET.get('state')
    shuxing = request.GET.get('shuxing')
    word = request.GET.get('word')

    print(type)
    print(state)
    print(shuxing)
    print(word)

    sql = 'select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id '
    if type == None and state == None and shuxing == None and word == None:
        sql = 'select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id '
    else:
        if (type != 'None' and type != 'all'):
            sql = sql + " AND " + 'b.kind_name' + " = '" + dict1[type] + "'"
        if (state != 'None' and state != 'all'):
            sql = sql + " AND " + 'a.book_state' + " = '" + dict2[state] + "'"
        if (shuxing != 'None' and shuxing != 'all'):
            sql = sql + " AND " + 'a.book_price' + " between '" + str(dict3[shuxing][0]) + "'AND'" + str(
                dict3[shuxing][1]) + "'"
        if (word != 'None' and word != 'all'):
            sql = sql + " AND " + "a.book_words" + " between '" + str(dict4[word][0]) + "'AND'" + str(
                dict4[word][1]) + "'"

    print(sql)
    cursor.execute(sql)
    Contacts = cursor.fetchall()
    random.shuffle(Contacts)
    paginator = Paginator(Contacts, 18)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    try:
        page1 = int(request.GET.get('page'))
    except:
        page1 = None

    if page1 != None:
        page = page1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except (EmptyPage):
        contacts = paginator.page(paginator.num_pages)
    index = contacts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index - 2 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'classify-row.html',
                  {'type': type, 'state': state, 'shuxing': shuxing, 'word': word, 'contacts': contacts,
                   'page_range': page_range, 'start_index': start_index, 'end_index': end_index, 'dict1': dict1,
                   'dict2': dict2, 'dict5': dict5, 'dict6': dict6})


def wanben(request):
    type = request.GET.get('type')
    state = request.GET.get('state')
    shuxing = request.GET.get('shuxing')
    word = request.GET.get('word')

    print(type)
    print(state)
    print(shuxing)
    print(word)

    sql = "select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id and a.book_state='完本'"
    if type == None and state == None and shuxing == None and word == None:
        sql = "select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id and a.book_state='完本'"
    else:
        if (type != 'None' and type != 'all'):
            sql = sql + " AND " + 'b.kind_name' + " = '" + dict1[type] + "'"
        # if (state != 'None' and state != 'all'):
        #     sql = sql + " AND " + 'a.book_state' + " = '" + dict2[state] + "'"
        if state == 'lianzai':
            sql = sql.replace("and a.book_state='完本'", "and a.book_state='连载中'")
        if (shuxing != 'None' and shuxing != 'all'):
            sql = sql + " AND " + 'a.book_price' + " between '" + str(dict3[shuxing][0]) + "'AND'" + str(
                dict3[shuxing][1]) + "'"

        if (word != 'None' and word != 'all'):
            sql = sql + " AND " + "a.book_words" + " between '" + str(dict4[word][0]) + "'AND'" + str(
                dict4[word][1]) + "'"

    print(sql)
    cursor.execute(sql)
    Contacts = cursor.fetchall()
    random.shuffle(Contacts)
    paginator = Paginator(Contacts, 12)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    try:
        page1 = int(request.GET.get('page'))
    except:
        page1 = None

    if page1 != None:
        page = page1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except (EmptyPage):
        contacts = paginator.page(paginator.num_pages)
    index = contacts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index - 2 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'wanben.html',
                  {'type': type, 'state': state, 'shuxing': shuxing, 'word': word, 'contacts': contacts,
                   'page_range': page_range, 'start_index': start_index, 'end_index': end_index, 'dict1': dict1,
                   'dict2': dict2, 'dict5': dict5, 'dict6': dict6})


def free(request):
    cursor.execute(
        "select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id and book_price>0")
    Contacts = cursor.fetchall()
    Contacts = Contacts[:9]
    print(Contacts)
    try:
        user_id = request.session['user_id']
        for i in Contacts:
            book_id = i['book_id']
            cursor.execute("select * from n_bookcase where user_id=%s and book_id=%s", [user_id, book_id, ])
            bookcase = cursor.fetchone()
            if bookcase == None:
                i['shujia'] = '加入书架'
            else:
                i['shujia'] = '已收藏'
    except:
        for i in Contacts:
            i['shujia'] = '加入书架'
    return render(request, 'time-free.html', {'Contacts': Contacts})


def freeAll(request):
    type = request.GET.get('type')
    state = request.GET.get('state')
    shuxing = request.GET.get('shuxing')
    word = request.GET.get('word')

    print(type)
    print(state)
    print(shuxing)
    print(word)

    sql = 'select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id and a.book_price=0'
    if type == None and state == None and shuxing == None and word == None:
        sql = 'select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id and a.book_price=0 '
    else:
        if (type != 'None' and type != 'all'):
            sql = sql + " AND " + 'b.kind_name' + " = '" + dict1[type] + "'"
        if (state != 'None' and state != 'all'):
            sql = sql + " AND " + 'a.book_state' + " = '" + dict2[state] + "'"

        if shuxing == 'fufei':
            sql = sql.replace('and a.book_price=0', 'and a.book_price>0')
        if (word != 'None' and word != 'all'):
            sql = sql + " AND " + "a.book_words" + " between '" + str(dict4[word][0]) + "'AND'" + str(
                dict4[word][1]) + "'"

    print(sql)
    cursor.execute(sql)
    Contacts = cursor.fetchall()
    random.shuffle(Contacts)
    paginator = Paginator(Contacts, 12)
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    try:
        page1 = int(request.GET.get('page'))
    except:
        page1 = None

    if page1 != None:
        page = page1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except (EmptyPage):
        contacts = paginator.page(paginator.num_pages)
    index = contacts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 2 if index >= 2 else 0
    end_index = index + 2 if index <= max_index - 2 else max_index
    page_range = paginator.page_range[start_index:end_index]

    return render(request, 'freeAll.html',
                  {'type': type, 'state': state, 'shuxing': shuxing, 'word': word, 'contacts': contacts,
                   'page_range': page_range, 'start_index': start_index, 'end_index': end_index, 'dict1': dict1,
                   'dict2': dict2, 'dict5': dict5, 'dict6': dict6})


def shoplog(request):
    return render(request, 'shoplog.html')


def shop(request):
    return render(request, 'shopping.html')


def dashang(request):
    return render(request, 'dashang.html')


def pay(request):
    return render(request, 'pay.html')


# 分词函数
def myjie():
    list = []
    print('=====================')
    cursor.execute(
        "select book_name,user_name,book_id,kind_name from n_bookinfo a,n_user b,n_kind c where a.user_id=b.user_id and a.kind_id=c.kind_id")
    result = cursor.fetchall()
    for row in result:

        id = row['book_id']
        ks = row['kind_name']
        r.sadd(ks, id)
        for item in row['book_name']:
            key = item
            r.sadd(key, id)
        for item in row['user_name']:
            key = item
            r.sadd(key, id)
        for item in row['kind_name']:
            key = item
            r.sadd(key, id)

        word_list = jieba.cut_for_search(row['book_name'])
        for data in word_list:
            key = data
            r.sadd(key, id)
        word_list = jieba.cut_for_search(row['user_name'])
        for data in word_list:
            key = data
            r.sadd(key, id)


# 搜索
def query(request):
    lst = []
    name = request.GET.get('keys')
    # name = request.POST.get('keyword')
    print(name)
    key = name
    s = r.smembers(key)
    print(s)
    for i in s:
        cursor.execute(
            "select * from n_bookinfo a,n_kind b,n_user c where a.kind_id=b.kind_id and a.user_id=c.user_id and book_id=%s",
            [i])

        result = cursor.fetchone()
        print(result)
        lst.append(result)

    print('====================')
    # print(lst)

    return render(request, 'search.html', {'message': lst})


def buy(request):
    try:
        user_id = request.session['user_id']
    except:
        return redirect('/login/')
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    book_id = request.GET.get('book_id')
    cursor.execute(
        "select * from n_bookinfo a,n_user b,n_kind c where a.user_id=b.user_id and a.kind_id=c.kind_id and book_id=%s",
        [book_id])
    result = cursor.fetchone()
    cursor.execute("insert into n_buyrecord (book_id,buy_time,user_id)values(%s,%s,%s)",
                   [result['book_id'], nowTime, user_id])
    conn.commit()
    return render(request, 'finished.html', {'message': '支付成功!'})


def record(request):
    alist = []
    info = ''
    try:
        user_id = request.session['user_id']
        info = 'in'
    except:
        return redirect('/login/')
    if info == 'in':
        cursor.execute("select * from n_buyrecord a,n_bookinfo b where a.book_id=b.book_id and a.user_id=%s", [user_id])
        result = cursor.fetchall()

        cursor.execute(
            "select max(read_id)  from n_readrecord a,n_bookinfo b  where a.book_id=b.book_id and a.user_id=%s group by a.book_id",
            [user_id])
        result1 = cursor.fetchall()
        print('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
        print(result1)
        for row in result1:
            cursor.execute(
                "select * from n_readrecord a,n_bookinfo b,n_chapter c where a.book_id=b.book_id  and a.chapter_id=c.chapter_id and read_id=%s",
                [row['max(read_id)']])
            dt = cursor.fetchone()
            alist.append(dt)
        print(alist)
    return render(request, 'shoplog.html', {'result': result, 'alist': alist})


def del_buy(request):
    id = request.GET.get('id')
    cursor.execute("delete  from n_buyrecord where buy_id=%s", [id])
    conn.commit()
    return redirect('/shoplog/')


def del_read(request):
    id = request.GET.get('id')
    cursor.execute("delete  from n_readrecord where book_id=%s ", [id])
    conn.commit()
    return redirect('/shoplog/')


# 周永辉
def author(request):
    # request.session['login_from']=request.META.get('HTTP_REFERER','/')
    # try:
    id = request.session['user_id']
    print(id)
    cursor.execute(
        "select * from n_user a,n_bookinfo b,n_kind c where a.user_id=b.user_id and b.kind_id=c.kind_id and a.user_id='%s' " % (
        id,))
    author = cursor.fetchall()

    print(author)
    num = len(author)
    # author = authorlist[0]
    from myapp.pager import Pagination
    current_page = request.GET.get('p')
    page_obj = Pagination(num, current_page)
    data_list = author[page_obj.start():page_obj.end()]
    return render(request, 'author.html', {'authorlist': data_list, 'page_obj': page_obj,'num':num})

    # return render(request, 'author.html', {'authorlist': author, 'author': author, 'num': num})
    # 直接输出错误信息
    # except Exception as error:
    #     print(error)
    #     return redirect('/login/')


def author_look(request):
    id = request.GET.get('user_id')

    cursor.execute(
        "select * from n_bookcase a,n_bookinfo b,n_user c,n_kind d where a.book_id=b.book_id and a.user_id=c.user_id and b.kind_id=d.kind_id and a.user_id='%s'" % (
        id,))
    caselist = cursor.fetchall()
    print(caselist)

    cursor.execute(
        "select * from n_user a,n_bookinfo b,n_kind c where a.user_id=b.user_id and b.kind_id=c.kind_id and a.user_id='%s'" % (
        id,))
    authorlist = cursor.fetchall()

    # print(authorlist)
    num = len(authorlist)
    author = authorlist[0]
    # print(author)
    if len(authorlist) >= 4:
        author_long = authorlist[0:4]
        print(author_long)
        return render(request, 'author_look.html',
                      {'author_long': author_long, 'num': num, 'author': author, 'caselist': caselist})
    else:
        return render(request, 'author_look.html',
                      {'authorlist': authorlist, 'author': author, 'num': num, 'caselist': caselist})

from django.http import JsonResponse
def login(request):
    if request.method == 'GET':
        # request.session['login_from'] = request.META.get('HTTP_REFERER', '/author/')
        return render(request, 'login.html')

    elif request.method == 'POST':
        user = request.POST.get('username')
        pwd = request.POST.get('password')

        conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        sql = "select * from n_useraccount,n_user where n_useraccount.user_id=n_user.user_id and user_account='%s'" % (
            user)
        cursor.execute(sql)
        messagelist = cursor.fetchone()
        print(messagelist)

        if messagelist == None:  # 防止用户名不正确，密码正确的情况
            return JsonResponse({'msg':'usererror'})
        elif messagelist['user_account']!=None and messagelist['user_password']!=pwd:
            return JsonResponse({'msg':'passerror'})
        elif pwd == messagelist['user_password'] and messagelist['user_account'] != None:
            id = messagelist['user_id']
            name = messagelist['user_name']
            request.session['user'] = user
            request.session['user_id'] = id
            request.session['user_name'] = name
            print(user, id, name)
            request.session.set_expiry(100000)
            # if request.POST.get('submit') == "登录":  # 点击按钮
            #     request.session.set_expiry(1000)  # session认证时间为1000s，1000s之后session认证失效
            # request.session['username'] = user  # user的值发送给session里的username
            request.session['is_login'] = True  # 认证为真
            return redirect('/main/')
            # return HttpResponseRedirect(request.session['login_from'])
        else:
            return redirect('/login/')


def loginout(request):
    try:
        del request.session['user']  # 清除session里的user
        del request.session['user_id']
        del request.session['user_name']
    except KeyError:
        pass
    return redirect('/main/')


def register(request):

    return render(request, 'register.html')

def judge(request):
    userphone=request.POST.get('userphone')
    password=request.POST.get('password')
    passwords=request.POST.get('passwords')
    message=request.POST.get('message')
    print(userphone,password,passwords,message)

    cursor.execute("select user_account from n_useraccount where user_account='%s'"%(userphone,))
    user=cursor.fetchall()
    print(user)
    flag = 'ok'

    if userphone=='':
        flag='kong'
        return HttpResponse(flag)

    if message=='':
        flag='nomsg'
        return HttpResponse(flag)
    if userphone:
        redismsg=r.get(userphone).decode('utf-8')
        print(redismsg)
        if message != redismsg:
            flag = 'msgerror'
            return HttpResponse(flag)

    if password==''or passwords=='':
        flag='nomi'
        return HttpResponse(flag)
    else:
        print(userphone)
        cursor.execute("select max(user_id) from n_useraccount")
        id=cursor.fetchone()
        maxid=id['max(user_id)']
        print(maxid)

        if user:
            flag='cunzai'
            return HttpResponse(flag)
        else:
            print(userphone)
            cursor.execute("insert into n_useraccount(user_account,user_password,user_id) values (%s,%s,%s)"%(userphone,password,maxid+1))
            conn.commit()

            import random
            xing = [
                '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
                '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
                '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
                '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
                '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
                '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
                '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']

            ming = [
                '的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
                '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
                '会', '家', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军', '乾', '坤', '美', '飘',
                '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快', '原',
                '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢',
                '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片', '罗',
                '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合', '反',
                '题', '必', '该', '论', '剧', '啊', '船', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰', '迹', '妹', '藸', '遍',
                '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡', '预', '盖', '释', '介', '烧', '误',
                '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误', ]
            a, b = [], []
            for i in range(1):
                x = random.randint(0, len(xing))
                m1 = random.randint(0, len(ming))
                m2 = random.randint(0, len(ming))
                name = '' + xing[x] + ming[m1] + ming[m2]
                a.append(name)
                print(a)
            b = a
            print(b[0])
            uname = b[0]

            cursor.execute("insert into n_user(user_id,user_name) values ('%s','%s')"%(maxid+1,uname))
            conn.commit()

            request.session['user_id']=maxid+1
            request.session['user_name']=uname
            request.session.set_expiry(100000)

            return HttpResponse(flag)
    # return HttpResponse(flag)




def send_message(request):
    from urllib import request as rq
    phone = request.POST.get('phone')
    identify = random.randint(100000, 999999)
    print(phone)
    textmod = {
               "sid": "d2ef97ce1db4e67d16389cbba451e413",    #云之讯Account Sid
               "token": "68cc68b10b469089946c653c9b9cfa72",  #云之讯Auth Token
               "appid": "2d99c17c9dab4e4387accff6be277aca",  #云之讯AppId
               "templateid": "396134",                         #短信模板
               "param": identify,
               "mobile": phone,
               "uid": phone
               }
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    req = rq.Request(url='https://open.ucpaas.com/ol/sms/sendsms', data=textmod, headers=header_dict)
    res = rq.urlopen(req)
    res = res.read().decode('utf-8')
    print(res)
    r.setex(phone, identify, 60)    #设置保存在redis的时间
    print(r.get(phone).decode('utf-8'))

    return HttpResponse(json.dumps(res))


def Reg(request):
    return render(request,'Reg.html')

def index(request):
    return  render(request,'index.html')

def Indexs(request):
    return  render(request,'Indexs.html')

def introduce(request):
    return render(request,'introduce.html')


def house_edit(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    id=request.GET.get('fyID')
    au_id=request.GET.get('auID')
    ad_id=request.GET.get('adID')
    boif_id=request.GET.get('boifID')
    chap_id=request.GET.get('chapID')

    cursor.execute("select chapter_content from n_examine where id='%s'"%(id,))
    content=cursor.fetchone()

    cursor.execute("select user_introduction from n_user where user_id='%s'"%(au_id,))
    author=cursor.fetchone()

    cursor.execute("select user_address from n_user where user_id='%s'" % (ad_id,))
    address = cursor.fetchone()

    cursor.execute("select book_introduction from n_bookinfo where book_id='%s'" % (boif_id,))
    intro = cursor.fetchone()

    cursor.execute("select chapter_content from n_chapter where chapter_id='%s'"%(chap_id,))
    chap_content=cursor.fetchone()

    return render(request,'house_edit.html',{'content':content,'id':id,'author':author,'au_id':au_id,'address':address,'ad_id':ad_id,'intro':intro,'boif_id':boif_id,'chap_content':chap_content,'chap_id':chap_id})

def house_list(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("select * from n_examine a,n_bookinfo b where a.book_id=b.book_id")
    list=cursor.fetchall()
    num=len(list)

    from myapp.pager import Pagination
    current_page = request.GET.get('p')
    page_obj = Pagination(num, current_page)
    data_list = list[page_obj.start():page_obj.end()]

    return render(request,'house_list.html',{'list':data_list,'num':num,'page_obj':page_obj})

def author_list(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("select * from n_user ")
    author = cursor.fetchall()
    a_num = len(author)

    from myapp.pager import Pagination
    current_page = request.GET.get('p')
    page_obj = Pagination(a_num, current_page)
    data_list = author[page_obj.start():page_obj.end()]

    return  render(request,'author_list.html',{'author':data_list,'a_num':a_num,'page_obj':page_obj})

def book_lsit(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("select * from n_kind a,n_examine_book b where a.kind_id=b.kind_id")
    book=cursor.fetchall()
    b_num=len(book)

    from myapp.pager import Pagination
    current_page = request.GET.get('p')
    page_obj = Pagination(b_num, current_page)
    data_list =book[page_obj.start():page_obj.end()]

    return render(request,'book_list.html',{'book':data_list,'b_num':b_num,'page_obj':page_obj})

def bookinfo_lsit(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("select * from n_kind a,n_bookinfo b,n_user c where a.kind_id=b.kind_id and b.user_id=c.user_id order by book_id asc")
    bookinfo = cursor.fetchall()
    boif_num = len(bookinfo)

    from myapp.pager import Pagination
    current_page = request.GET.get('p')
    page_obj = Pagination(boif_num, current_page)
    data_list = bookinfo[page_obj.start():page_obj.end()]

    return render(request, 'bookinfo_list.html', {'bookinfo': data_list, 'boif_num': boif_num,'page_obj':page_obj})

def chapter_list(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("select chapter_id,chapter_name,book_name,user_name,chapter_content from n_chapter a,n_bookinfo b,n_user c where a.book_id=b.book_id and b.user_id=c.user_id order by chapter_id desc limit 45")
    chapter=cursor.fetchall()
    chap_num=len(chapter)

    from myapp.pager import Pagination
    current_page = request.GET.get('p')
    page_obj = Pagination(chap_num, current_page)
    data_list = chapter[page_obj.start():page_obj.end()]

    return render(request,'chapter_list.html',{'chapter':data_list,'chap_num':chap_num,'page_obj':page_obj})


def loupanchart(request):
    return render(request,'loupanchart.html')


def Logins(request):
    if request.method=='GET':
        return render(request,'Logins.html')

    if request.method=='POST':
        name=request.POST.get('username')
        password=request.POST.get('password')

        if name=='':
            return render(request,'Logins.html')
        else:
            cursor.execute("select * from n_useraccount where user_account='%s'"%(name,))
            user=cursor.fetchone()
            if user=='':
               return render(request, 'Logins.html')
            else:
                if user['user_password']!=password:
                    return render(request, 'Logins.html')
                else:

                    return render(request,'Indexs.html',{'username':user})

def search(request):
    text=request.POST.get('text')
    print(text)
    cursor.execute("select * from n_user where user_name='%s' or user_id='%s' or user_sex='%s'"%(text,text,text,))
    find=cursor.fetchall()
    print(find)
    num=len(find)

    if find==():
        cursor.execute("select * from n_bookinfo a,n_user b,n_kind c  where a.user_id=b.user_id and a.kind_id=c.kind_id and (book_id='%s' or book_name='%s' or kind_name='%s')"%(text,text,text,))
        bookinfo=cursor.fetchall()
        num=len(bookinfo)
        print(bookinfo)

        from myapp.pager import Pagination
        current_page = request.GET.get('p')
        page_obj = Pagination(num, current_page)
        data_list=bookinfo[page_obj.start():page_obj.end()]
        return render(request, 'find.html', { 'bookinfo': data_list, 'num': num, 'page_obj': page_obj})
    else:
        from myapp.pager import Pagination
        current_page = request.GET.get('p')
        page_obj = Pagination(num, current_page)
        data_list = find[page_obj.start():page_obj.end()]
        return render(request,'find.html',{'find':data_list,'num':num,'page_obj':page_obj})


def delete(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    id=request.GET.get('fyID')
    au_id=request.GET.get('auID')
    bo_id=request.GET.get('boID')
    chap_id=request.GET.get('chapID')
    boif_id=request.GET.get('boifID')

    print(id,au_id,bo_id,chap_id)
    if id:
        cursor.execute("delete from n_examine where id='%s'" % (id,))
        conn.commit()
        return redirect('/house_list/')
    elif au_id:
        cursor.execute("delete from n_user where user_id='%s'"%(au_id,))
        conn.commit()
        return redirect('/author_list/')
    elif bo_id:
        cursor.execute("delete from n_examine_book where book_id='%s'" % (bo_id,))
        conn.commit()
        return redirect('/book_list/')
    elif chap_id:
        cursor.execute("delete from n_chapter where chapter_id='%s'" % (chap_id,))
        conn.commit()
        return redirect('/chapter_list/')
    elif boif_id:
        cursor.execute("delete from n_bookinfo where book_id='%s'" % (boif_id,))
        conn.commit()
        return redirect('/bookinfo_list/')


def updata(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    id=request.GET.get('fyID')
    ad_id=request.GET.get('adID')
    au_id=request.GET.get('auID')
    boif_id=request.GET.get('boif_id')

    content=request.POST.get('content')

    if id:
        print(content)
        sql1=("update n_examine set chapter_content='%s'"%(content,))
        sql2=("where id='%s'"%(id,))
        sql=sql1+sql2
        cursor.execute(sql)
        conn.commit()
        return redirect('/house_list/')

    if ad_id:
        sql1 = ("update n_user set user_address='%s'" % (content,))
        sql2 = ("where user_id='%s'" % (ad_id,))
        sql = sql1 + sql2
        cursor.execute(sql)
        conn.commit()
        return redirect('/author_list/')

    if au_id:
        sql1 = ("update n_user set user_introduction='%s'" % (content,))
        sql2 = ("where user_id='%s'" % (au_id,))
        sql = sql1 + sql2
        cursor.execute(sql)
        conn.commit()
        return redirect('/author_list/')

    if boif_id:
        print(content)
        sql1 = ("update n_bookinfo set book_introduction='%s'" % (content,))
        sql2 = ("where book_id='%s'" % (boif_id,))
        sql = sql1 + sql2
        cursor.execute(sql)
        conn.commit()
        return redirect('/bookinfo_list/')


def add(request):
    conn = pymysql.connect("139.196.136.63", "user1", "123456", "kuyue", charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    id=request.GET.get('fyID')
    au_id=request.GET.get('auID')
    bo_id=request.GET.get('boID')

    if id:
        cursor.execute("select max(chapter_id) from n_chapter ")
        chapter_id=cursor.fetchone()['max(chapter_id)']

        print(chapter_id)

        cursor.execute("select * from n_examine where id='%s'"%(id,))
        content=cursor.fetchone()
        print(content)
        book_id=content['book_id']
        chapter_content=content['chapter_content']
        chapter_name=content['chapter_name']

        cursor.execute("insert into n_chapter(chapter_id,chapter_name,chapter_content,book_id) values (%s,%s,%s,%s)",[chapter_id+1,chapter_name,chapter_content,book_id])
        conn.commit()

        cursor.execute("delete from n_examine where id='%s'" % (id,))
        conn.commit()

        return redirect('/house_list/')

    if bo_id:
        cursor.execute("select max(book_id) from n_bookinfo ")
        book_id = cursor.fetchone()['max(book_id)']

        cursor.execute("select * from n_examine_book where book_id='%s'" % (bo_id,))
        book = cursor.fetchone()
        print(book)

        name= book['book_name']
        words=book['book_introduction']
        state=book['book_state']
        image=book['book_image']
        ticket=book['book_ticketcount']
        sell=book['book_sellcount']
        price=book['book_price']
        user_id=book['user_id']
        click=book['book_clickcount']
        estimco=book['book_estimatecount']
        estim=book['book_estimate']
        kind=book['kind_id']

        cursor.execute("insert into n_bookinfo(book_id,book_name,book_introduction,book_state,book_image,book_ticketcount,book_sellcount,book_price,user_id,book_clickcount,book_estimatecount,book_estimate,kind_id) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       [book_id+1,name,words,state, image, ticket,sell,price,user_id,click,estimco,estim,kind])
        conn.commit()

        cursor.execute("delete from n_examine_book where book_id='%s'" % (bo_id,))
        conn.commit()

        return redirect('/book_list/')




from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def listing(request):

    cursor.execute("select * from n_bookinfo")
    info=cursor.fetchall()
    num=len(info)
    print(info)
    print(num)

    from myapp.pager import Pagination
    current_page = request.GET.get('p')
    page_obj = Pagination(num, current_page)
    data_list = info[page_obj.start():page_obj.end()]
    return render(request, 'list.html', {'data': data_list, 'page_obj': page_obj})