# coding:utf-8
import datetime
import json
import re
import threading
import time
import uuid
import sys
from redis import Redis
import os
import traceback
from functools import wraps
from html.parser import HTMLParser
from threading import Thread

import pymysql
import requests
import queue
import logging
import wrapt
import hashlib
from lxml import etree

from random import choice

try:
    redis_db = Redis(host='127.0.0.1', port=6379, decode_responses=True)
except:
    pass
L = threading.Lock()
Q = queue.Queue()
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
requests.packages.urllib3.disable_warnings()
adapter = requests.adapters.HTTPAdapter(pool_connections=1000, pool_maxsize=1000)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, bytes):
            return obj.decode()
        else:
            return json.JSONEncoder.default(self, obj)


def async_pool(max_thread):
    def start_async(f):
        def wrapper(*args, **kwargs):
            while 1:
                func_thread_active_count = len([i for i in threading.enumerate() if i.name == f.__name__])
                if func_thread_active_count < max_thread:
                    thr = Thread(target=f, args=args, kwargs=kwargs, name=f.__name__)
                    thr.start()
                    break
                else:
                    time.sleep(0.01)

        return wrapper

    return start_async


def async_(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs, name=f.__name__)
        thr.start()

    return wrapper


def cache(seconds=0, is_update=None, redis_db=redis_db):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        # 将实参进行md5作为key
        md5 = hashlib.md5()
        md5.update(bytes("%s" % (args), encoding='utf-8'))
        key = md5.hexdigest()
        func_name = wrapped.__name__
        key = "%s:%s" % (func_name, key)

        # 如果不更新则直接走缓存
        if not is_update:
            res = redis_db.get(key)
            if res:
                return json.loads(res)
        res = wrapped(*args, **kwargs)
        if seconds > 0:
            redis_db.set(key, json.dumps(res, cls=CJsonEncoder), ex=seconds)
        else:
            redis_db.set(key, json.dumps(res, cls=CJsonEncoder))
        return res

    return wrapper


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time() * 1000
        result = function(*args, **kwargs)
        t1 = time.time() * 1000
        print('running %s : %sms ' % (function.__name__, str(int(t1 - t0))))
        return result

    return function_timer


class Tool:
    def __init__(self, db="", is_proxy_pool=False, is_session=False):
        self.db = db
        self.db_config = {
            "host": 'localhost',
            "port": 3306,
            "user": 'root',
            "password": ''
        }
        self.html = ''
        self.selector = ''
        self.send_queue_name = ''
        self.receive_queue_name = ''
        self.host_name = '127.0.0.1'
        self.port = 5672
        self.username = 'guest'
        self.password = 'guest'
        self.proxy_pool = []
        self.extend_proxy_pool = []
        self.cursor = ''
        self.conn = None

        if not is_session:
            self.session = requests
        else:
            self.session = requests.session()
            self.session.mount('http://', adapter)
            self.session.mount('https://', adapter)
            self.session.verify = False
        if is_proxy_pool:
            self.update_proxy_pool()
            while True:
                if self.proxy_pool:
                    break
                else:
                    time.sleep(0.01)

    def md5(self, text: str):
        '''
        md5字符串
        :param info:字符串
        :return: 经过hash过的字符串
        '''
        import hashlib

        md5 = hashlib.md5()
        md5.update(bytes(text, encoding='utf-8'))
        return md5.hexdigest()

    def get_xpath(self, selector, xpath, is_list=True):
        '''
        通过传入的xpath语法获取内容
        :param selector: etree.HTML(html)
        :param xpath: xpath语法
        :param is_list: 返回值是否为list
        :return: value
        '''
        value = selector.xpath(xpath)
        if not is_list:
            if not value:
                value = ''
            else:
                value = value[0]
        return value

    def get_re(self, text, regex, is_list=True):
        '''
        通过传入的正则表达式以及文本获取内容
        :param text: 字符串
        :param regex: 正则表达式
        :param is_list: 返回值是否为list
        :return: value
        '''
        value = re.findall(re.compile(regex, re.S), text)  # list
        if not is_list:
            if not value:
                value = ''
            else:
                value = value[0]
        return value

    def replace_label(self, text):
        '''
        去除字符串中的转义符号
        :param text: 字符串
        :return: 去除转义符号后的字符串
        '''
        text = text.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '').replace('\xa0', '')
        return text

    def get_html(self, url, headers={}, proxy={}, cookies={}, data={}, params={}, timeout=5, debug=False):

        for i in range(5):
            try:
                res = self.session.get(url, headers=headers, timeout=timeout, proxies=proxy, cookies=cookies, data=data, verify=False, params=params)
                return res
            except Exception as e:
                if debug:
                    logging.info(e)
        else:
            return False

    def post_html(self, url, headers={}, data={}, json={}, proxy={}, cookies={}, timeout=5, debug=False):

        for i in range(5):
            try:
                res = self.session.post(url, data=data, json=json, headers=headers, timeout=timeout, proxies=proxy, cookies=cookies, verify=False)
                return res
            except Exception as e:
                if debug:
                    logging.info(e)
        else:
            return False

    def translate(self, html):
        '''
        把selector转成html
        :param html:
        :return:
        '''
        content = etree.tostring(html, method='html').decode()
        content = HTMLParser().unescape(content)
        return content

    def get_uuid(self):
        '''
        获取uuid1
        :return:
        '''
        return str(uuid.uuid1()).replace('-', '')

    @staticmethod
    def get_nowTime():
        '''
        获取当前标准时间
        :return:
        '''
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def get_con(self):
        while 1:
            try:
                connection = pymysql.connect(host=self.db_config['host'], port=self.db_config['port'], user=self.db_config['user'], password=self.db_config['password'],
                                             db=self.db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
                return connection
            except Exception as e:
                print(e)
                time.sleep(0.5)

    def get_cursor(self):
        if not self.conn:
            self.conn = self.get_con()
        try:
            cursor = self.conn.cursor()
        except:
            self.conn = self.get_con()
            cursor = self.get_cursor()

        return cursor

    def to_underline(self, data: dict):
        '''
        dict 驼峰转下划线
        :param data:
        :return:
        '''
        new_data = {}
        for i in data:
            p = re.compile(r'([a-z]|\d)([A-Z])')
            sub = re.sub(p, r'\1_\2', i).lower()
            new_data[sub] = data[i]
        return new_data

    def to_hump(self, data: dict):
        '''
        dict 下划线转驼峰
        :param data:
        :return:
        '''
        new_data = {}
        for i in data:
            sub = re.sub(r'(_\w)', lambda x: x.group(1)[1].upper(), i)
            new_data[sub] = data[i]
        return new_data

    def save_result(self, table_name: str, data: dict or list):
        '''
        存库
        :param table_name:存入数据库表的名称
        :param data: 数据
        :return: None
        '''
        res = 0
        if isinstance(data, dict):
            data = [data]
        if isinstance(data, list):
            data_list = data
            L.acquire()
            cursor = self.get_cursor()
            for index, data in enumerate(data_list):
                key = []
                values = []
                for i in data:
                    if isinstance(data[i], int) or isinstance(data[i], float) or isinstance(data[i], bytes):
                        key.append(i)
                        values.append('%s' % data[i])
                    elif isinstance(data[i], str):
                        key.append(i)
                        values.append('"%s"' % pymysql.escape_string(data[i]))
                    elif data[i] or data[i] == 0:
                        key.append(i)
                        values.append('"%s"' % data[i])
                key = ','.join(key)
                values = ','.join(values)
                sql = 'insert into %s (%s) VALUES (%s)' % (table_name, key, values)
                try:
                    res = cursor.execute(sql)
                except Exception as e:
                    if 'PRIMARY' not in str(e):
                        print(e)
                        print(sql[:300])
            self.conn.commit()
            cursor.close()
            L.release()
        return res

    def form_data(self, form):
        str_form = ''
        for i in form:
            if not form[i]: continue
            str_form += '%s=%s&' % (i, form[i])
        return str_form

    def to_datetime(self, int_time):
        '''
        时间戳转成标准格式的时间
        :param int_time:
        :return:
        '''
        int_time = int(int_time)
        date_time = time.localtime(int_time)
        date_time = time.strftime('%Y-%m-%d %H:%M:%S', date_time)
        return date_time

    def to_unixtime(self, date_time):
        '''
        标准格式的时间转成时间戳
        :param date_time:
        :return:
        '''
        date_time = str(date_time)
        unix_time = time.strptime(date_time, "%Y-%m-%d %H:%M:%S")
        unix_time = int(time.mktime(unix_time))
        return unix_time

    def get_today(self):
        '''
        获取今天的日期
        :return:
        '''
        today = str(datetime.date.today())
        return today

    def get_yesterday(self):
        today = datetime.date.today()
        yesterday = str(today + datetime.timedelta(days=-1))
        return yesterday

    def get_nextday(self):
        today = datetime.date.today()
        nextday = str(today + datetime.timedelta(days=1))
        return nextday

    def get_betweenday(self, begin_date):
        date_list = []
        begin_date = datetime.datetime.strptime(str(begin_date), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime("%Y-%m-%d")
            date_list.append(date_str)
            begin_date += datetime.timedelta(days=1)
        return date_list

    def con(self, sql):
        L.acquire()
        cursor = self.get_cursor()
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            if not res:
                res = []
        except Exception as e:
            print(e, sql)
            res = []
        finally:
            cursor.close()
            self.conn.commit()
            L.release()

        return res

    def con_execute(self, sql):
        L.acquire()
        try:
            cursor = self.get_cursor()
            if isinstance(sql, str):
                cursor.execute(sql)
            elif isinstance(sql, list):
                for i, v in enumerate(sql):
                    cursor.execute(v)
                    self.print_rate_of_progress(i, len(sql))
            self.conn.commit()
        except Exception as e:
            print(e, "\n", sql[:500])
        finally:
            cursor.close()
            L.release()

    def b64_enc_text(self, text: str):
        '''
        base64加密
        :param text:
        :return:
        '''
        import base64

        return base64.b64encode(text.encode())

    def b64_dec_text(self, text: str):
        '''
        base64解密
        :param text:
        :return:
        '''
        import base64

        return base64.b64decode(text.encode()).decode()

    @async_
    def mq_send_mes(self, data, send_queue_name=False, host='127.0.0.1', replay_to=''):
        import pika

        count = 0
        if self.send_queue_name and not send_queue_name:
            send_queue_name = self.send_queue_name
        while 1:
            try:
                # credentials = pika.PlainCredentials(username=self.username, password=self.password)
                credentials = pika.PlainCredentials(username="sqh", password="123456")
                pro_parameters = pika.ConnectionParameters(host=host, port=self.port, credentials=credentials)
                pro_connection = pika.BlockingConnection(parameters=pro_parameters)
                pro_channel = pro_connection.channel()
                pro_channel.queue_declare(queue=send_queue_name, durable=True)
                pro_channel.basic_publish(exchange='', routing_key=send_queue_name, body=json.dumps(data, cls=CJsonEncoder),
                                          properties=pika.BasicProperties(content_encoding='utf-8', content_type='text/plain', reply_to=replay_to))
                break
            except Exception as e:
                print(e)
                count += 1
                if count > 5:
                    return False
                time.sleep(1)

    def mq_receive_mes(self, callback, receive_queue_name=''):
        '''
        :param callback: ch, method, properties, body
        :return:
        '''
        import pika

        if self.receive_queue_name and not receive_queue_name:
            receive_queue_name = self.receive_queue_name
        try:
            # 设置端口
            credentials = pika.PlainCredentials(username=self.username, password=self.password)
            parameters = pika.ConnectionParameters(host=self.host_name, port=self.port, credentials=credentials)
            connection = pika.BlockingConnection(parameters=parameters)
            # 声明一个通道，在通道里发送消息
            channel = connection.channel()
            channel.queue_declare(receive_queue_name, durable=True)
            channel.basic_consume(receive_queue_name, callback, auto_ack=True)
            print('[%s] waiting for msg .' % (receive_queue_name))
            channel.start_consuming()  # 开始循环取消息
        except Exception as e:
            print(e)
            time.sleep(1)
            self.mq_receive_mes(callback, receive_queue_name)

    def mq_return_mes(self, ch, properties, data):
        import pika

        ch.basic_publish(exchange='',
                         routing_key=properties.reply_to,
                         properties=pika.BasicProperties(content_encoding='utf-8', content_type='text/plain'),
                         body=json.dumps(data, cls=CJsonEncoder))

    def get_regr(self, param_list, result_list):
        from sklearn import linear_model
        if not isinstance(param_list[0], list):
            param_list = [[i] for i in param_list]
        regr = linear_model.LinearRegression()
        regr.fit(param_list, result_list)
        return regr

    def regr_guess(self, regr, except_data, flat_type=True):
        res = regr.predict([[except_data]])[0]
        if flat_type == True:
            res = (round((res) * 1000)) / 10
        return res

    def get_float(self, value, number=2):
        number = 10 ** number
        return round(value * number) / number

    def show_plot(self, x, y, regr):
        import matplotlib.pyplot as plt
        import pandas as pd
        plt.scatter(x, y, color='blue')
        plt.plot(x, regr.predict(pd.SparseArray(x).values.reshape(-1, 1)), color='red', linewidth=4)
        plt.show()

    def get_logistic_regr(self, x, y):
        from sklearn import linear_model
        if not isinstance(x[0], list):
            x = [[i] for i in x]
        regr = linear_model.LogisticRegression(solver='liblinear')
        regr.fit(x, y)
        return regr

    def get_non_linear_regr(self, x, y, degree=2):
        from sklearn import linear_model
        from sklearn.preprocessing import PolynomialFeatures
        import numpy as np
        length = len(x)
        x = np.array(x).reshape([length, 1])
        y = np.array(y)
        poly_reg = PolynomialFeatures(degree=degree)  # degree=2表示二次多项式
        X_poly = poly_reg.fit_transform(x)  # 构造datasets_X二次多项式特征X_poly
        lin_reg_2 = linear_model.LinearRegression()  # 创建线性回归模型
        lin_reg_2.fit(X_poly, y)  # 使用线性回归模型学习X_poly和datasets_Y之间的映射关系
        return lin_reg_2

    def show_non_linear_plot(self, x, y, model, degree=2):
        import numpy as np
        import matplotlib.pyplot as plt
        from sklearn.preprocessing import PolynomialFeatures
        length = len(x)
        x = np.array(x).reshape([length, 1])
        y = np.array(y)
        minX = min(x)  # 以数据datasets_X的最大值和最小值为范围，建立等差数列，方便后续画图
        maxX = max(x)
        X = np.arange(minX, maxX).reshape([-1, 1])
        poly_reg = PolynomialFeatures(degree=degree)  # degree=2表示二次多项式
        plt.scatter(x, y, color='orange')
        plt.plot(X, model.predict(poly_reg.fit_transform(X)), color='blue')
        plt.show()

    def division(self, x, y, number=2):
        return round(x / y, number)

    def print_rate_of_progress(self, index, total):
        print('进度：%s/%s   %s%%' % (index, total, self.division(index * 100, total)))

    def get_ssim(self, a, b):
        '''
        :param a: x
        :param b: y
        :return: a和b的相似度
        '''
        import difflib

        return difflib.SequenceMatcher(None, a, b).quick_ratio()

    def queue_add_data(self, form, data):
        Q.put()

    def get_proxy(self):
        proxy = self.con('select * from local.proxy where error_count < 2 order by rand() limit 1')[0]
        id = proxy['id']
        proxy = "%s:%s" % (proxy['ip'], proxy['port'])
        proxy = {
            "http": proxy,
            "https": proxy,
        }
        return id, proxy

    @async_
    def update_proxy_pool(self):
        while True:
            proxies = self.con('select * from proxy')
            L.acquire()
            self.proxy_pool = []
            for proxy in proxies:
                proxy = {
                    "http": "http://%s" % (proxy['proxy']),
                    "https": "https://%s" % (proxy['proxy']),
                }
                self.proxy_pool.append(proxy)
            L.release()
            time.sleep(10)

    def get_webdriver(self, path, is_onload_img=False):
        from selenium import webdriver

        os.environ["webdriver.chrome.driver"] = path
        chrome_options = webdriver.ChromeOptions()
        if not is_onload_img:
            prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
            # chrome_options.add_argument("user-data-dir=C:\\Users\Administrator\AppData\Local\Google\Chrome\\User Data")
            chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(path, chrome_options=chrome_options)
        return driver

    def post_email(self, text, email_name, subject="预测报警"):
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr
        # 发件人邮箱账号
        my_sender = 'duhongyu@sqhtech.com'
        # user登录邮箱的用户名，password登录邮箱的密码（授权码，即客户端密码，非网页版登录密码），但用腾讯邮箱的登录密码也能登录成功
        my_pass = 'du15511370945A'
        # 收件人邮箱账号
        my_user = 'duhongyu@sqhtech.com'

        ret = True
        try:
            # 邮件内容
            msg = MIMEText(text, 'plain', 'utf-8')
            # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['From'] = formataddr([email_name, my_sender])
            # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['To'] = formataddr(["开发者", my_user])
            # 邮件的主题
            msg['Subject'] = subject

            # SMTP服务器，腾讯企业邮箱端口是465，腾讯邮箱支持SSL(不强制)， 不支持TLS
            # qq邮箱smtp服务器地址:smtp.qq.com,端口号：456
            # 163邮箱smtp服务器地址：smtp.163.com，端口号：25
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            # 登录服务器，括号中对应的是发件人邮箱账号、邮箱密码
            server.login(my_sender, my_pass)
            # 发送邮件，括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.sendmail(my_sender, [my_user, ], msg.as_string())
            # 关闭连接
            server.quit()
            # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            print('邮件发送成功')
        except Exception as e:
            print("邮件发送失败", e)
            ret = False
        return ret

    def create_path(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def dup_insert(self, table: str, datas: dict or list) -> list:
        """
        无则插入, 有则更新
        :param table: 表名
        :param datas: 数据
        :return:
        """

        def analysis_dict(item, type="install"):
            if type == "install":
                key = item.keys()
                value = item.values()
                return ", ".join(key), ", ".join(["\"{}\"".format(pymysql.escape_string(v) if isinstance(v, str) else v) for v in value])
            elif type == "update":
                str_list = ["{}=\"{}\"".format(k, pymysql.escape_string(v) if isinstance(v, str) else v) for k, v in item.items()]
                return ", ".join(str_list)

        insert_url = """INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {}"""
        if isinstance(datas, dict):
            datas = [datas]
        res = 0
        if isinstance(datas, list):
            L.acquire()
            try:
                if not self.conn:
                    self.conn = self.get_con()
                cursor = self.conn.cursor()
                for data in datas:
                    key, value = analysis_dict(data, type="install")
                    kv_up = analysis_dict(data, type="update")
                    sql = insert_url.format(table, key, value, kv_up)
                    try:
                        res = cursor.execute(sql)
                    except Exception as e:
                        print(e, sql)
                self.conn.commit()
                cursor.close()
            finally:
                L.release()
        return res

    def save_many_data_mysql(self, table, data_list):
        '''
        :return:
        '''
        if not isinstance(data_list, list):
            data_list = [data_list]
        keys = data_list[0].keys()
        sql = "insert into %s (%s) values " % (table, ",".join(keys))
        insert_sql_list = []
        # 对数组进行切片，每3W条为一个SQL
        new_data_list = []
        split_count = 30000
        for i in range(0, len(data_list), split_count):
            new_data_list.append(data_list[i: (i + split_count)])

        for data in data_list:
            values = []
            for key in keys:
                value = data.get(key, "")
                if isinstance(value, int) or isinstance(value, float) or isinstance(value, bytes):
                    value = '%s' % value
                elif isinstance(value, str):
                    value = '"%s"' % pymysql.escape_string(value)
                elif value or value == 0:
                    value = '"%s"' % value
                values.append(value)
            values = ','.join(values)
            insert_sql = "(%s)" % values
            insert_sql_list.append(insert_sql)
        insert_sql_list = ",".join(insert_sql_list)
        sql += insert_sql_list
        self.con_execute(sql)


if __name__ == '__main__':
    tool = Tool('local')
    print(len('style="width:220px;word-break: break-all;"'))
