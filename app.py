# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template, url_for
import pymysql
import os
from datetime import datetime
import uuid
import json

app = Flask(__name__)
# 文件上传保存根路径
UP_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")


@app.route('/')
def index():
    print(UP_DIR)
    return render_template("index.html")


@app.route('/book/list', methods=['GET', 'POST'])
def book_list():
    if request.method == 'GET':
        creator = request.args.get('creator')
        print(creator)
        db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="testbrowser")
        sql = "select id, bookname, author, publisher from library where creator='{0}'".format(creator)
        cursor = db.cursor()
        result = []
        try:
            cursor.execute(sql)
            data = cursor.fetchall()  # 嵌套元组数据,无数据返回空元组
            if data:
                temp = {}
                for i in data:
                    temp["id"] = i[0]
                    temp["author"] = i[2]
                    temp['bookname'] = i[1]
                    temp["publisher"] = i[3]
                    result.append(temp.copy())
        except BaseException:
            print('获取图书数据失败')
        finally:
            db.close()
        return jsonify(result)
    if request.method == 'POST':
        data = request.get_json()
        # print(data['bookname'], data['author'], data['publisher'], data['creator'])
        db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="testbrowser")
        cursor = db.cursor()
        sql = "insert into library(bookname, author, publisher, creator) values('{0}', '{1}', '{2}', '{3}') ".format(data['bookname'], data['author'], data['publisher'], data['creator'])
        try:
            cursor.execute(sql)
            db.commit()
            print('插入成功')
        except BaseException:
            db.rollback()
            print('插入失败')
            db.close()
            return jsonify(dict(ok='-1'))
        finally:
            db.close()
        return jsonify(dict(ok='1'))


@app.route('/book/list/<int:bookId>', methods=['DELETE', 'GET', 'PUT'])
def book_delete(bookId=0):
    if request.method == 'DELETE':
        print(bookId)
        db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="testbrowser")
        cursor = db.cursor()
        sql = "delete from testbrowser.library where id={0}".format(bookId)
        # print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print('删除成功')
        except BaseException:
            db.rollback()
            print('删除失败')
            db.close()
            return jsonify(dict(message='数据删除失败'))
        finally:
            db.close()
        return jsonify(dict(message='数据成功删除'))

    if request.method == 'GET':
        print(bookId)
        db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="testbrowser")
        cursor = db.cursor()
        sql = "select bookname, author, publisher, creator,id from library where id={0}".format(bookId)
        # print(sql)
        try:
            cursor.execute(sql)
            data = cursor.fetchone()
            db.commit()
            print(data)
            list_name = ['bookname', 'author', 'publisher', 'creator', 'id']
            data_dict = dict(zip(list_name, list(data)))
            print(data_dict)
            print('获取成功')
        except BaseException:
            db.rollback()
            db.close()
            print('获取失败')
            return jsonify(dict(message='数据获取失败'))
        finally:
            db.close()
        return jsonify(dict(data_dict))

    if request.method == 'PUT':
        print(bookId)
        data = request.get_json()
        print(data['bookname'], data['author'], data['publisher'], data['creator'])
        db = pymysql.connect(host="127.0.0.1", user="root", password="123456", database="testbrowser")
        cursor = db.cursor()
        sql = "update library set bookname='{0}',author='{1}', publisher='{2}', creator='{3}' where id={4}".format(data['bookname'], data['author'], data['publisher'], data['creator'], bookId)
        print(sql + '修改sql')
        try:
            cursor.execute(sql)
            db.commit()
            print('修改成功')
        except BaseException:
            db.rollback()
            print('修改失败')
            db.close()
            return jsonify(dict(ok='-1'))
        finally:
            db.close()
        return jsonify(dict(ok='1'))


# 允许上传的文件，以及文件格式校验
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ['png', 'jpg', 'jpeg', 'gif']


# 唯一文件名无后缀
def gen_rnd_filename():
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex)


@app.route('/uploads', methods=['POST', 'GET'])
def uploads_picture():
    if request.method == 'POST':
        print('你传图片来了啊')
        fd = request.files.get('img')
        print('=====上传图片数据')
        print(fd)
        if not allowed_file(fd.filename):                     # 图片格式不支持，上传图片失败
            return jsonify(dict(message='我要图片,你报错了哦'))
        my_name, fext = os.path.splitext(fd.filename)
        print(my_name, fext)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(UP_DIR, rnd_name)
        dirname = os.path.dirname(filepath)                      # 上级目录路径
        if not os.path.exists(dirname):                          # 不存在则创建目录
            os.makedirs(dirname)
        fd.save(filepath)                                        # 保存图片到服务器
        img_url = url_for('static', filename='%s/%s' % ('uploads', rnd_name))
        return jsonify(dict(url=img_url, filename=rnd_name, message='图片又过来了'))
    return render_template('uploadsPicture.html')


@app.route('/user/info', methods=['POST', 'GET', 'PUT'])
def user_info():
    if request.method == 'GET' and request.args.get("creator"):
        # flag=request.args.get("creator") == 'suifeng'
        # img_url = request.files.get('imgUrl')
        print('我收到你get请求了,我不去弄数据库了，给你个json数据接口吧')
        img_url = request.args.get("imgUrl")
        print(img_url)
        return jsonify(dict(email='1234@12.com', nickname='suifen', gender=1, desc='nihaoa', imgUrl=img_url))
    if request.method == 'PUT':
        print('我收到你的put请求了')
        print(request.files)
        fd = request.files.get('head-portrait')
        if not allowed_file(fd.filename):                     # 如果图片格式不支持，上传图片失败
            return jsonify(dict(message='我要图片,你报错了哦'))
        my_name, fext = os.path.splitext(fd.filename)
        print(my_name, fext)
        rnd_name = '%s%s' % (gen_rnd_filename(), fext)
        filepath = os.path.join(UP_DIR, 'user/', rnd_name)
        dirname = os.path.dirname(filepath)                      # 上级目录路径
        if not os.path.exists(dirname):                          # 不存在则创建目录
            os.makedirs(dirname)
        fd.save(filepath)                                        # 保存图片到服务器
        img_url = url_for('static', filename='%s/%s' % ('uploads/user', rnd_name))
        return jsonify(dict(url=img_url, filename=rnd_name, message='上传图片过来了'))
    return render_template('user_info.html')


if __name__ == '__main__':
    app.run()
