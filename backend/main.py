from datetime import date
import functools
from logging import error
import os

from db import *

from flask import Flask, session
from flask import redirect
from flask import request, make_response
from flask import render_template
from flask import url_for
from flask import jsonify
from flask.json.tag import PassDict
from flask_cors import CORS
from werkzeug.wrappers import response

from flask_cors import cross_origin

import json
import jwt
import time

from jwt import exceptions

# 生成一个app
app = Flask(__name__)
# app.secret_key = 'lab3'
# CORS(app)
CORS(app, resources={r"/*": {"origins":"*"}}, send_wildcard=True)
# app.config["CORS_HEADERS"] = "Content-Type"

# use dic to simulate user database
db_source = {
    'user_table': {
        'root': {
            'pwd': '457213'
        }
    }, 
    'user_info_table': {
        'dawsonenjoy': {
            'age': 18
        }
    }
}

db = None

# function and variable defined to jwt

SECRET_KEY = "asgfddasdasdasgerher"

def create_token(name):
    '''基于jwt创建token的函数'''
    global SECRET_KEY
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    exp = int(time.time() + 60 * 60)
    payload = {
        "name": name,
        "exp": exp
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm='HS256', headers=headers)
    # 返回生成的token
    return token

def make_return_json(info, msg):
    # print(msg)
    global db
    if msg == None:
        return json.dumps({'code': 20000, 'data': info})
    elif msg == 'token已失效':
        db_close(db)
        return json.dumps({'code': 50014, 'message': msg})
    elif msg == 'token认证失败':
        db_close(db)
        return json.dumps({'code': 50008, 'message': msg})
    else:
        return json.dumps({'code': 50000, 'message': str(msg)})

def validate_token(token):
    '''校验token的函数，校验通过则返回解码信息'''
    global SECRET_KEY
    payload = None
    msg = None
    try:
        payload = jwt.decode(token, SECRET_KEY, 'HS256')
        # payload = jwt.decode(token, SECRET_KEY, True)
        # jwt有效、合法性校验
    except exceptions.ExpiredSignatureError:
        msg = 'token已失效'
    except jwt.DecodeError:
        msg = 'token认证失败'
    except jwt.InvalidTokenError:
        msg = '非法的token'
    return (payload, msg)

def return_all_loan_record(db):
    info = search_start_loan(db)
    return_info = []
    for row in info:
        if(row[3] == 0):
            return_info.append([row[0], row[1], row[2], 'not begin'])
        elif(row[3] < row[2]):
            return_info.append([row[0], row[1], row[2], 'in process'])
        else:
            return_info.append([row[0], row[1], row[2], 'finish'])
    info = search_not_start_loan(db)
    for row in info:
        return_info.append([row[0], row[1], row[2], 'not begin'])
    return return_info

def handle_info_filter(info, filter):
    print(info)
    season_map = {'1':'s1', '2':'s1', '3':'s1', '4':'s2', '5':'s2', '6':'s2','7':'s3', '8':'s3', '9':'s3', '10':'s4', '11':'s4', '12':'s4'}
    date_dict = {}
    if(filter == 'month'):
        for row in info:
            date = row[1].strftime('%Y-%m')
            if date in date_dict:
                info = date_dict[date]
                date_dict[date] = [info[0], date, info[2] + row[3], info[3] + row[4]]
            else:
                date_dict[date] = [row[0], date, row[3], row[4]]
    elif (filter == 'season'):
        for row in info:
            year = row[1].year
            month = row[1].month
            date = str(year) + '-' + season_map[str(month)]
            if date in date_dict:
                info = date_dict[date]
                date_dict[date] = [info[0], date, info[2] + row[3], info[3] + row[4]]
            else:
                date_dict[date] = [row[0], date, row[3], row[4]]
    else:
        for row in info:
            date = row[1].strftime('%Y')
            if date in date_dict:
                info = date_dict[date]
                date_dict[date] = [info[0], date, info[2] + row[3], info[3] + row[4]]
            else:
                date_dict[date] = [row[0], date, row[3], row[4]]
    return_info = []
    for key in date_dict:
        return_info.append(date_dict[key])
    return return_info

# router function to handle frontend request

# 对app执行请求页面地址到函数的绑定
@app.route("/", methods=("GET", "POST"))
@cross_origin()
def root():
    return redirect('/login')

@app.route("/login", methods = ("GET", "POST"))
@cross_origin()
def login():
    # print("\n\n\n\ntest\n\n\n\n")
    data = request.get_json()
    username = data['username']
    passwd = data['password']
    print(username)
    print(passwd)
    global db
    db = db_login(username, passwd, '127.0.0.1', 'bank_system')
    if(db == None):
        print('login fail')
        return json.dumps({'status': 1, 'code': 50008, 'msg': '用户名或密码错误！'}, ensure_ascii=False)
    else:
        print('\n\nsuccess login')
        token = create_token(username)
        return json.dumps({'status': 1, 'code': 20000, 'data': {'token': token, 'code': 20000}})

@app.route("/user_info", methods=(["GET", "POST"]))
@cross_origin()
def get_user_info():
    print(request)
    print('\n\n\n\ntesttest\n\n\n')
    data = request.get_json()
    print(data)
    info = {
        'roles': ['admin'],
        'introduction': 'I am a super administrator',
        'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        'name': 'Super Admin'
    }
    return json.dumps({'code': 20000, 'data': info})

@app.route("/guest/search", methods=(["GET", "POST"]))
@cross_origin()
def guest_search():
    data = request.get_json()
    print(data)
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    attribute, information, error = search_guest(db, data)
    # print(attribute)
    print(information)
    if error == 1:
        return json.dumps({'code': 50008, 'msg': information})
    else:
        return make_return_json(information, msg)

@app.route("/guest/add", methods=(["GET", "POST"]))
@cross_origin()
def guest_add():
    data = request.get_json()
    token = request.headers['myToken']
    # token = data['token']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    print(data)
    tel = data['tel']
    contact_tel = data['contact_tel']
    if(len(tel) != 11 or len(contact_tel)!= 11):
        info = 'invalid telephone length!'
        return make_return_json(info, info)
    info, error = add_guest(db, data)
    if error == 1:
        return make_return_json(info, info)
    else:
        information = get_update_db(db, 'Client')
        return make_return_json(information, msg)

@app.route("/guest/delete", methods=(["POST", "GET"]))
@cross_origin()
def guest_delete():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    print(data)
    info, error = delete_guest(db, data)
    if error == 1:
        return make_return_json(info, info)
    else:
        information = get_update_db(db, 'Client')
        return make_return_json(information, msg)

@app.route("/guest/update", methods=(["GET", "POST"]))
@cross_origin()
def guest_update():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    old_value = data['old_value']
    new_value = data['new_value']
    if(len(new_value['tel']) != 11 or len(new_value['contact_tel']) != 11):
        info = 'invalid tel length'
        return make_return_json(info, info)
    if(old_value['Client_ID'] != new_value['Client_ID']):
        info = 'invalid update on Client_ID'
        return make_return_json(info, info)
    info, error = update_guest(db, new_value)
    if error == 1:
        return make_return_json(info, info)
    else:
        information = get_update_db(db, 'Client')
        print(information)
        return make_return_json(information, msg)

@app.route("/account/add_saving", methods=(["POST", "GET"]))
@cross_origin()
def account_add_saving():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info, error = add_saving_account(db, data)
    if error == 1:
        return make_return_json(info, info)
    else:
        info = search_all_account(db)
        return make_return_json(info, msg)

@app.route("/account/add_checking", methods=(["POST", "GET"]))
@cross_origin()
def account_add_checking():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info, error = add_checking_account(db, data)
    if error == 1:
        return make_return_json(info, info)
    else:
        info = search_all_account(db)
        return make_return_json(info, msg)

@app.route("/account/search_account", methods=(["POST", "GET"]))
@cross_origin()
def account_search():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info, error = search_account(db, data)
    # print(info)
    return make_return_json(info, msg)

@app.route("/account/delete_account", methods=(["POST", "GET"]))
@cross_origin()
def delete_account():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    balance = data['balance']
    if(balance != 0):
        info = 'can\'t delete account with money'
        return make_return_json(info, info)
    count_type = data['count_type']
    if count_type == 0:
        print('in delete saving')
        info, error = delete_saving_account(db, data)
    elif count_type == 1:
        print('in delete checking')
        info, error = delete_checking_account(db, data)
    if error == 1:
        return make_return_json(info, info)
    else:
        info = search_all_account(db)
        return make_return_json(info, msg)

@app.route("/account/get_account_info", methods=(["POST", "GET"]))
@cross_origin()
def get_account_info():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    count_type = data['count_type']
    if count_type == 0:
        info, error = search_saving_account(db, data)
    elif count_type == 1:
        info, error = search_checking_account(db, data)
    if error == 1:
        return make_return_json(info, info)
    else:
        return make_return_json(info, msg)

@app.route("/account/update_saving_account", methods=(["POST", "GET"]))
@cross_origin()
def saving_account_update():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    old_value = data['old_value']
    new_value = data['new_value']
    print(new_value)
    print(old_value)
    if(new_value['Client_ID'] != old_value['Client_ID']):
        info = 'invalid change in Client ID'
        return make_return_json(info, info)
    elif(new_value['account_id'] != old_value['account_id']):
        info = 'invalid change in account id'
        return make_return_json(info, info)
    info, error = update_saving_account(db, new_value, old_value)
    if(error == 1):
        return make_return_json(info, info)
    else:
        info = search_all_account(db)
        return make_return_json(info, None)

@app.route("/account/update_checking_account", methods=(["POST", "GET"]))
@cross_origin()
def checking_account_update():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    old_value = data['old_value']
    new_value = data['new_value']
    print(new_value)
    print(old_value)
    if(new_value['Client_ID'] != old_value['Client_ID']):
        info = 'invalid change in Client ID'
        return make_return_json(info, info)
    elif(new_value['account_id'] != old_value['account_id']):
        info = 'invalid change in account id'
        return make_return_json(info, info)
    info, error = update_checking_account(db, new_value, old_value)
    if(error == 1):
        return make_return_json(info, info)
    else:
        info = search_all_account(db)
        return make_return_json(info, None)

@app.route("/account/get_account_detail", methods=(["POST", "GET"]))
@cross_origin()
def account_detail():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info, error = get_account_detail(db, data)
    print(info)
    return_info = []
    return_info.append(['bank_name', info[0]])
    return_info.append(['account_id', info[1]])
    return_info.append(['balance', info[2]])
    return_info.append(['opendate', info[3].strftime('%Y-%m-%d')]) 
    return_info.append(['recent_visit_date', info[4].strftime('%Y-%m-%d')])
    if(info[5] == 0):
        return_info.append(['count_type', 'saving account'])
        return_info.append(['interest_rate', info[7]])
        return_info.append(['currency_type', info[8]])
    else:
        return_info.append(['count_type', 'checking account'])
        return_info.append(['over_draft', info[7]])
    
    # infom = []
    # infom.append(return_info)
    if(error == 1):
        return make_return_json(info, info)
    else:
        return make_return_json(return_info, None)

@app.route("/loan/add", methods=(["POST", "GET"]))
@cross_origin()
def loan_add():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info, error = add_loan(db, data)
    if error == 1:
        return make_return_json(info, info)
    else:
        return_info = return_all_loan_record(db)
        return make_return_json(return_info, msg)

@app.route("/loan/get_list", methods=(["POST", "GET"]))
@cross_origin()
def loan_get_list():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    return_info = return_all_loan_record(db)
    return make_return_json(return_info, None)

@app.route("/loan/add_pay_loan", methods=(["POST", "GET"]))
@cross_origin()
def pay_loan_add():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info, error = add_pay_loan(db, data)
    if(error == 1):
        return make_return_json(info, info)
    else:
        return_info = return_all_loan_record(db)
        return make_return_json(return_info, msg)

@app.route("/loan/loan_detail", methods=(["POST", "GET"]))
@cross_origin()
def loan_detail():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info = get_loan_detail(db, data)
    return make_return_json(info, None)

@app.route("/loan/delete", methods=(["POST", "GET"]))
@cross_origin()
def loan_delete():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    loan_status = data['loan_status']
    if(loan_status != 'finish'):
        info = 'Can\'t delete unfinished loan !'
        return make_return_json(info, info)
    info, error = delete_loan(db, data)
    if(error == 1):
        return make_return_json(info, info)
    else:
        return_info = return_all_loan_record(db)
        return make_return_json(return_info, msg)

@app.route("/loan/search", methods=(["POST", "GET"]))
@cross_origin()
def loan_search():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    loan_status = data['loan_status']
    if(loan_status == 'not begin'):
        info = search_not_start_loan_condition(db, data)
        return_info = []
        for row in info:
            return_info.append([row[0], row[1], row[2], 'not begin'])
        return make_return_json(return_info, msg)
    elif (loan_status == 'in process'):
        info = search_start_loan_condition(db, data)
        return_info = []
        for row in info:
            if(row[2] > row[3]):
                return_info.append([row[0], row[1], row[2], 'in process'])
        return make_return_json(return_info, msg)
    elif(loan_status == 'finish'):
        info = search_start_loan_condition(db, data)
        return_info = []
        for row in info:
            if(row[2] == row[3]):
                return_info.append([row[0], row[1], row[2], 'finish'])
        return make_return_json(return_info, msg)
    else:
        return_info = []
        info = search_not_start_loan_condition(db, data)
        for row in info:
            return_info.append([row[0], row[1], row[2], 'not begin'])
        info = search_start_loan_condition(db, data)
        for row in info:
            if(row[2] == row[3]):
                return_info.append([row[0], row[1], row[2], 'finish'])
            else:
                return_info.append([row[0], row[1], row[2], 'in process'])
        return make_return_json(return_info, msg)

@app.route("/statistics/get_logfile", methods=(["POST", "GET"]))
@cross_origin()
def logfile_get():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    info = get_logfile(db)
    return_info = []
    for row in info:
        return_info.append([row[0], row[1].strftime('%Y-%m-%d'), row[2], row[3], row[4]])
    print(return_info)
    return make_return_json(return_info, msg)

@app.route("/statistics/get_saving_record", methods=(["POST", "GET"]))
@cross_origin()
def saving_record():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    bank_name = data['bank_name']
    filter = data['filter']
    info = get_saving_by_bank_name(db, bank_name)
    return_info = handle_info_filter(info, filter)
    print(return_info)
    return make_return_json(return_info, msg)

@app.route("/statistics/get_loan_record", methods=(["POST", "GET"]))
@cross_origin()
def loan_record():
    data = request.get_json()
    token = request.headers['myToken']
    payload, msg = validate_token(token)
    if msg != None:
        return make_return_json(msg, msg)
    name = payload['name']
    passwd = db_source['user_table'][name]['pwd']
    db = db_login(name, passwd, '127.0.0.1', 'bank_system')
    print(data)
    bank_name = data['bank_name']
    filter = data['filter']
    info = get_loan_by_bank_name(db, bank_name)
    return_info = handle_info_filter(info, filter)
    print(return_info)
    return make_return_json(return_info, msg)

#返回不存在页面的处理
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

if __name__ == "__main__":

    app.run(host = "0.0.0.0", debug=True, port=int(os.getenv('PORT', 4444)))