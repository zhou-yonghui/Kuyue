"""Kuyue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('Read/', views.Read),
    path('Header/', views.Header),
    path('Details/', views.Details),
    path('Talk/', views.Talk),
    path('TalkDetails/', views.TalkDetails),
    path('MyTalk/', views.MyTalk),
    path('Likes1/', views.Likes1),
    path('Likes2/', views.Likes2),
    path('pingfen/', views.pingfen),
    path('shujia/', views.shujia),
    path('toupiao/', views.toupiao),
    path('Write_book/', views.Write_book),

    # 马容
    path('main/', views.main),
    path('ranking/', views.ranking),
    path('ranking/ticket/', views.ranking_ticket),
    path('ranking/sell/', views.ranking_sell),
    path('ranking/len/', views.ranking_len),
    path('ranking/click/', views.ranking_click),
    # path('search/', views.search),
    # path('timefree/', views.timefree),
    path('self/', views.self),
    path('selfset/', views.selfset),
    path('getProvince/', views.getProvince),
    path('getCity/', views.getCity),
    path('getDistrict/', views.getDistrict),
    # 周磊
    path('classify/', views.classify),
    path('classify-row/', views.row),
    path('wanben/', views.wanben),
    path('free/', views.free),
    path('freeAll/', views.freeAll),
    path('shoplog/', views.record),
    path('shop/', views.shop),
    # path('dashang/', views.dashang),
    path('pay/', views.pay),
    path('query/', views.query),
    path('buy/', views.buy),
    path('del_buy/', views.del_buy),
    path('del_read/', views.del_read),
    # 周永辉
    path('author/', views.author),
    path('author_look/', views.author_look),
    path('login/', views.login),
    path('loginout/', views.loginout),
    path('register/', views.register),
    path('judge/',views.judge),
    path('send_message/',views.send_message),

    # 测试
    # path('test1/', views.test1),
    path('index/',views.index),

    path('Indexs/',views.Indexs),
    path('introduce/',views.introduce),
    path('house_list/',views.house_list),
    path('author_list/',views.author_list),
    path('book_list/',views.book_lsit),
    path('house_edit/',views.house_edit),
    path('Logins/',views.Logins),
    path('loupanchart/',views.loupanchart),
    path('delete/',views.delete),
    path('update/',views.updata),
    path('add/',views.add),
    path('find/',views.search),
    path('bookinfo_list/',views.bookinfo_lsit),
    path('chapter_list/',views.chapter_list),

    path('Reg/',views.Reg),
    path('listing/',views.listing),
]
