from django.shortcuts import render
from django.db import connection
import random
from django.shortcuts import redirect
from django.shortcuts import reverse
from . import models
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
import time
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
# Create your views here.
import os
import os.path as osp

ROOT_PAHT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
FRONT_PATH = osp.join(ROOT_PAHT, 'front')
UTILS_PATH = osp.join(ROOT_PAHT, 'utils')


def get_corsor():
    return connection.cursor()


# Create your views here.
def index(request):
    cursor = get_corsor()
    cursor.execute("select book_id, book_name, author from front_book")
    books = cursor.fetchall()
    return render(request, 'index.html', context={"books": books})


def book_info(request):
    Books = models.Book.objects.all()
    if request.POST.get('alter_book_info'):    # 修改图书信息
        id = request.POST.get("id")
        newurl = '/alter_book_info/' + id
        return redirect(newurl, locals())
    elif request.POST.get('delete_book'):    # 删除图书
        id = request.POST.get("id")     # 点击表格中哪个图书的删除返回的id就是该图书
        book = models.Book.objects.get(book_id=id)
        if book.total_number > 0:    # 只有在图书库存数量为0时，才可以删除书目
            return render(request, 'error_delete_book.html', locals())
        else:
            models.Book.objects.filter(book_id=id).delete()
            Books = models.Book.objects.all()
    elif request.POST.get('search_book'):
        # 通过层层筛选最终剩下符合搜索条件的数据，其中__icontains表示包含，不区分大小写
        if request.POST.get("book_name"):
            book_name = request.POST.get("book_name")
            Books = Books.filter(book_name__icontains=book_name)
        if request.POST.get("ISBN"):
            ISBN = request.POST.get("ISBN")
            Books = Books.filter(ISBN__icontains=ISBN)
        if request.POST.get("publisher"):
            publisher = request.POST.get("publisher")
            Books = Books.filter(publisher__icontains=publisher)
        if request.POST.get("author"):
            author = request.POST.get("author")
            Books = Books.filter(author__icontains=author)
        if request.POST.get("label"):
            label = request.POST.get("label")
            Books = Books.filter(label__icontains=label)
        if request.POST.get("can_borrow"):
            can_borrow = request.POST.get("can_borrow")
            Books = Books.filter(can_borrow=can_borrow)

    return render(request, 'book_info.html', locals())


def user_info(request):
    Users = models.User.objects.all()

    if request.POST.get('alter_user_info'):
        id = request.POST.get("id")
        newurl = '/alter_user_info/' + id
        return redirect(newurl, locals())
    elif request.POST.get('borrow_book'):    # 借阅图书
        id = request.POST.get("id")
        newurl = '/borrow_book/' + id
        return redirect(newurl, locals())
    elif request.POST.get('delete_user'):    # 删除图书
        id = request.POST.get("id")
        user = models.User.objects.get(user_id=id)
        if user.book_number > 0:    # 只有在图书库存数量为0时，才可以删除书目
            return render(request, 'error_delete_user.html', locals())
        else:
            models.User.objects.filter(user_id=id).delete()
            Users = models.User.objects.all()
    elif request.POST.get('search_user'):
        if request.POST.get("user_name"):
            user_name = request.POST.get("user_name")
            Users = Users.filter(user_name__icontains=user_name)
        if request.POST.get("tele"):
            tele = request.POST.get("tele")
            Users = Users.filter(tele__icontains=tele)
        if request.POST.get("user_type"):
            user_type = int(request.POST.get("user_type"))
            Users = Users.filter(user_type=user_type)

    return render(request, 'user_info.html', locals())


def add_book(request):
    if request.method == 'GET':
        return render(request, 'add_book.html')
    else:
        try:
            book_id = random.randint(0, 10000)
            while models.Book.objects.all().filter(book_id=book_id):  # 防止生成相同book_id
                book_id = random.randint(0, 10000)
            book_name = request.POST.get("book_name")
            if request.POST.get("ISBN"):
                ISBN = request.POST.get("ISBN")
            else:
                ISBN = 'Unknow'
            if request.POST.get("publisher"):
                publisher = request.POST.get("publisher")
            else:
                publisher = 'Unknow'
            if request.POST.get("publish_date"):
                publish_date = request.POST.get("publish_date")
            else:
                publish_date = 'Unknow'
            if request.POST.get("author"):
                author = request.POST.get("author")
            else:
                author = 'Unknow'
            if request.POST.get("label"):
                label = request.POST.get("label")
            else:
                label = 'Unknow'
            total_number = int(request.POST.get("total_number"))
            if total_number>0:
                can_borrow = 'Y'
            else:
                can_borrow = 'N'
            cursor = get_corsor()
            cursor.execute(
                "insert into front_book(book_id, book_name, ISBN, publish_date, author, label, current_number, total_number, can_borrow, publisher) values('%d','%s','%s','%s','%s','%s','%d','%d', '%s', '%s')" % (
                    book_id, book_name, ISBN, publish_date, author, label, total_number, total_number, can_borrow, publisher))
        except:
            pass
        # 跳转到首页
        Books = models.Book.objects.all()
        return redirect('/book_info/', locals())


def add_user(request):
    if request.method == 'GET':
        return render(request, 'add_user.html')
    else:
        try:
            user_id = random.randint(10000, 20000)
            while models.User.objects.all().filter(user_id=user_id):  # 防止生成相同user_id
                user_id = random.randint(10000, 20000)
            user_name = request.POST.get("user_name")
            user_type = int(request.POST.get("user_type"))
            tele = request.POST.get("tele")
            cursor = get_corsor()
            cursor.execute(
                "insert into front_user(user_id, user_name, user_type, tele, book_number) values('%d','%s','%d','%s','%d')" % (
                    user_id, user_name, user_type, tele, 0))
        except:
            pass
        # 跳转到首页
        Users = models.User.objects.all()
        return redirect('/user_info/', locals())


def alter_user_info(request):
    cur_url = str(request.path)
    splited_url = cur_url.split('/')
    id = splited_url[-1]
    if request.method == 'GET':
        return render(request, 'add_user.html', locals())
    else:
        user = models.User.objects.get(user_id=id)
        if request.POST.get("user_name"):
            user.user_name = request.POST.get("user_name")
        if request.POST.get("user_type"):
            user.user_type = int(request.POST.get("user_type"))
        if request.POST.get("tele"):
            user.tele = request.POST.get("tele")

        user.save()
        Users = models.User.objects.all()
        return redirect('/user_info/', locals())


def alter_book_info(request):
    cur_url = str(request.path)
    splited_url = cur_url.split('/')
    id = splited_url[-1]
    if request.method == 'GET':
        return render(request, 'add_book.html', locals())
    else:
        book = models.Book.objects.get(book_id=id)
        if request.POST.get("book_name"):
            book.book_name = request.POST.get("book_name")
        if request.POST.get("ISBN"):
            book.ISBN = request.POST.get("ISBN")
        if request.POST.get("publisher"):
            book.publisher = request.POST.get("publisher")
        if request.POST.get("publish_date"):
            book.publish_date = request.POST.get("publish_date")
        if request.POST.get("author"):
            book.author = request.POST.get("author")
        if request.POST.get("label"):
            book.label = request.POST.get("label")
        if request.POST.get("total_number"):
            new_total_number = int(request.POST.get("total_number"))
            if new_total_number >= book.total_number or book.total_number - new_total_number <= book.current_number:  # 有新书入库
                book.current_number += new_total_number - book.total_number
                book.total_number = new_total_number

            else:   # 出库数量不应该大于图书馆现拥有数目
                return render(request, 'error_alter_book.html', locals())
        if book.current_number <= 0:
            # models.Book.objects.filter(book_id=id).update(can_borrow='N')
            book.can_borrow = 'N'
        else:
            book.can_borrow = 'Y'
        book.save()
        Books = models.Book.objects.all()
        return redirect('/book_info/', locals())
        # return render(request, 'book_info.html', locals())


def borrow_book(request):
    cur_url = str(request.path)
    splited_url = cur_url.split('/')
    user_id = int(splited_url[-1])  # user_id是url的最后一项
    # 将该用户所有借阅信息取出
    user_borrow = models.Borrow.objects.filter(user_id=user_id, is_return=0)
    user_return = models.Borrow.objects.filter(user_id=user_id, is_return=1)
    if request.POST.get('return_book'):    # 归还图书
        book_id = int(request.POST.get("id"))    # book_id为点击进去的某一项图书对应的id
        # 更新归还信息, 下面选择的含义是选择含有目标user_id，book_id并且没有归还的第一个条目，防止用一个人借了好几本相同的书
        borrow = models.Borrow.objects.filter(user_id=user_id, book_id=book_id, is_return=0).first()
        borrow.is_return = 1
        borrow.return_time = str(time.asctime(time.localtime(time.time())))
        borrow.save()
        # 更新图书current_number
        book = models.Book.objects.get(book_id=book_id)
        book.current_number += 1
        # 更新书籍可以借阅与否状态
        if book.current_number > 0:
            book.can_borrow = 'Y'
        book.save()
        # 更新用户book_number
        user = models.User.objects.get(user_id=user_id)
        user.book_number -= 1
        user.save()

    elif request.POST.get('confirm_borrow_book'):
        book_id = int(request.POST.get("id"))    # book_id为点击进去的某一项图书对应的id
        book_name = models.Book.objects.get(book_id=book_id).book_name
        borrow_id = random.randint(20000, 30000)
        borrow_time = str(time.asctime(time.localtime(time.time())))
        return_time = 'Unknow'
        user = models.User.objects.get(user_id=user_id)
        if (user.user_type == 1 and user.book_number >= 8) or (user.user_type == 0 and user.book_number >= 4):
            # 超出借书限制
            return render(request, 'error_borrow_book.html', locals())
        # 添加借阅记录
        borrow = models.Borrow(
            borrow_id=borrow_id,
            user_id=user_id,
            book_id=book_id,
            book_name=book_name,
            is_return=0,
            borrow_time=borrow_time,
            return_time='Unknow',
        )
        borrow.save()
        # 更新图书current_number
        book = models.Book.objects.get(book_id=book_id)
        book.current_number -= 1
        # 更新书籍可以借阅与否状态
        if book.current_number <= 0:
            book.can_borrow = 'N'
        book.save()
        # 更新用户book_number
        user = models.User.objects.get(user_id=user_id)
        user.book_number += 1
        user.save()

    Books = models.Book.objects.filter(current_number__gt=0)  # 查找现存数量大于0的图书
    Borrowed_Books = []
    for item in user_borrow:
        Borrowed_Books.extend(list(models.Book.objects.filter(book_id=item.book_id)))
    return render(request, 'borrow_book.html', locals())


def batch_book_in(request):
    Books = models.Book.objects.all()
    if request.method == 'GET':
        return render(request, 'batch_book_in.html', locals())
    else:
        # 通过request.POST.getlist把全部
        book_id = request.POST.getlist("id")
        book_in = request.POST.getlist("in_number")
        # print(book_id, type(book_id), len(book_id))
        # print(book_in, type(book_in), len(book_in))
        for i in range(len(book_id)):
            book = models.Book.objects.get(book_id=book_id[i])
            in_number = request.POST.getlist("in_number")[i]
            if in_number:  # 如果含有修改的值
                in_number = int(in_number)
                book.total_number += in_number
                book.current_number += in_number
                if book.current_number <= 0:  # 更新可借阅状态
                    book.can_borrow = 'N'
                else:
                    book.can_borrow = 'Y'
                book.save()
        Books = models.Book.objects.all()
        return render(request, 'batch_book_in.html', locals())


def batch_book_out(request):
    Books = models.Book.objects.all()
    if request.method == 'GET':
        return render(request, 'batch_book_out.html', locals())
    else:
        # 通过request.POST.getlist把全部
        book_id = request.POST.getlist("id")
        for i in range(len(book_id)):
            book = models.Book.objects.get(book_id=book_id[i])
            out_number = request.POST.getlist("out_number")[i]
            if out_number:  # 如果含有修改的值
                out_number = int(out_number)
                if out_number <= book.current_number:
                    book.total_number -= out_number
                    book.current_number -= out_number
                else:  # 出库数量需要小于current_number
                    pass
                if book.current_number <= 0:  # 更新可借阅状态
                    book.can_borrow = 'N'
                else:
                    book.can_borrow = 'Y'
                book.save()
        Books = models.Book.objects.all()
        return render(request, 'batch_book_out.html', locals())


def batch_import_book(request):
    Books = models.Book.objects.all()
    if request.method == 'GET':
        return render(request, 'batch_import_book.html')
    else:
        location = request.POST.get("location")
        if location:
            try:
                df_books = pd.read_csv(location)
            except:
                return render(request, 'error_batch_import.html', locals())
        else:
            df_books = pd.read_csv(osp.join(UTILS_PATH, 'books.csv'))
        for i in range(len(df_books.index)):
            book_id = random.randint(0, 10000)
            while models.Book.objects.all().filter(book_id=book_id):
                book_id = random.randint(0, 10000)
            book_name = df_books.book_name[i]
            # 使用pd.notnull判断是否为nan
            if pd.notnull(df_books.ISBN[i]):
                print(df_books.ISBN[i], type(df_books.ISBN[i]), np.float64('nan'), type(np.float64('nan')))
                ISBN = df_books.ISBN[i]
            else:
                ISBN = 'Unknow'
            if pd.notnull(df_books.publisher[i]):
                publisher = df_books.publisher[i]
            else:
                publisher = 'Unknow'
            if pd.notnull(df_books.publish_date[i]):
                publish_date = df_books.publish_date[i]
            else:
                publish_date = 'Unknow'
            if pd.notnull(df_books.author[i]):
                author = df_books.author[i]
            else:
                author = 'Unknow'
            if pd.notnull(df_books.label[i]):
                label = df_books.label[i]
            else:
                label = 'Unknow'
            total_number = int(df_books.total_number[i])
            if total_number>0:
                can_borrow = 'Y'
            else:
                total_number = 'N'
            cursor = get_corsor()
            cursor.execute(
                "insert into front_book(book_id, book_name, ISBN, publish_date, author, label, current_number, total_number, can_borrow, publisher) values('%d','%s','%s','%s','%s','%s','%d','%d', '%s', '%s')" % (
                    book_id, book_name, ISBN, publish_date, author, label, total_number, total_number, can_borrow, publisher))
    # 跳转到首页
    Books = models.Book.objects.all()
    return redirect('/book_info/', locals())


def batch_import_user(request):
    Users = models.Book.objects.all()
    if request.method == 'GET':
        return render(request, 'batch_import_user.html')
    else:
        location = request.POST.get("location")
        if location:
            try:
                df_users = pd.read_csv(location)
            except:
                return render(request, 'error_batch_import.html', locals())
        else:
            df_users = pd.read_csv(osp.join(UTILS_PATH, 'user.csv'))
        for i in range(len(df_users.index)):
            user_id = random.randint(10000, 20000)
            while models.User.objects.all().filter(user_id=user_id):  # 防止生成相同user_id
                user_id = random.randint(10000, 20000)
            user_name = df_users.user_name[i]
            user_type = int(df_users.user_type[i])
            tele = df_users.tele[i]
            cursor = get_corsor()
            cursor.execute(
                "insert into front_user(user_id, user_name, user_type, tele, book_number) values('%d','%s','%d','%s','%d')" % (
                    user_id, user_name, user_type, tele, 0))

        # 跳转到首页
    Users = models.User.objects.all()
    return redirect('/user_info/', locals())
