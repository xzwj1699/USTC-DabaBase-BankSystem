from functools import update_wrapper
from os import curdir
import MySQLdb
from MySQLdb._exceptions import OperationalError
from flask.scaffold import F
from flask_cors.core import flexible_str

import datetime

passwd = {'root': '457213'}


def db_login(user, passwd, server_addr, dbname):
    try:
        db = MySQLdb.connect(server_addr, user, passwd, dbname, charset = "utf8")
    except OperationalError:
        db = None

    return db

def db_showtable(db):
    cursor = db.cursor()
    cursor.execute("show tables")
    tabs = cursor.fetchall()
    res = list()
    for tab in tabs:
        cursor.execute("select count(*) from " + tab[0])
        row_cnt = cursor.fetchone()

        res.append((tab[0], row_cnt[0]))
    
    cursor.close()

    return res

# guest search function

def get_update_db(db, table):
    cursor = db.cursor()
    select_all = 'select * from ' + table
    cursor.execute(select_all)
    information = cursor.fetchall()
    return information

def search_add_condition(select, condition, where_flag, and_flag, filter):
    if(filter[condition] != ''):
        if(where_flag == False):
            select = select + 'where '
            where_flag = True
        if(and_flag == True):
            select = select + ' and '
        else:
            and_flag = True
        select = select + condition + ' like \'%' + filter[condition] + '%\' '
    return select, where_flag, and_flag

def search_guest(db, filter:dict):
    cursor = db.cursor()
    cursor.execute("desc Client")
    table_attributes = cursor.fetchall()
    attribute = []
    for item in table_attributes:
        attribute.append(item[0])
    select = "select * from Client "
    and_flag = False
    where_flag = False
    for condition in attribute:
        select, where_flag, and_flag = search_add_condition(select, condition, where_flag, and_flag, filter)
    print(select)
    try:
        cursor.execute(select)
        information = cursor.fetchall()
        error = 0
        return attribute, information, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        error = 1
        return attribute, e, error
    # print(attribute)

def delete_guest(db, values):
    cursor = db.cursor()
    Client_ID = values['Client_ID']
    check_linking_account = 'select count(*) from Client_Account where Client_ID = ' + Client_ID
    cursor.execute(check_linking_account)
    linking_exist = cursor.fetchall()
    if linking_exist[0][0] != 0:
        error = 1
        return 'Client has linking account', error
    cursor.execute("desc Client")
    table_attributes = cursor.fetchall()
    attribute = []
    for item in table_attributes:
        attribute.append(item[0])
    delete = 'delete from Client where '
    # delete_condition = []
    # print(values)
    # for attr in attribute:
    #     condition =  attr + ' = ' + '\'' + values[attr] + '\''
    #     delete_condition.append(condition)
    # delete = delete + ' and '.join(delete_condition)
    delete = delete + 'Client_ID = \'' + Client_ID + '\''
    print(delete)
    try:
        cursor.execute(delete)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def update_guest(db, new_value):
    cursor = db.cursor()
    cursor.execute("desc Client")
    table_attributes = cursor.fetchall()
    attribute = []
    for item in table_attributes:
        attribute.append(item[0])
    update = 'update Client set '
    set_condition = []
    Client_ID = new_value.pop('Client_ID')
    for attr in attribute:
        if(attr == 'Client_ID'):
            continue
        if(attr == 'name'):
            new_value[attr] = new_value[attr].replace('\'', '\\\'')
            print(new_value[attr])
        s_condition = attr + ' = ' + '\'' + new_value[attr] + '\''
        set_condition.append(s_condition)
    update = update + ' , '.join(set_condition) + ' where ' + 'Client_ID = ' + '\'' + Client_ID + '\''
    try:
        cursor.execute(update)
        print(update)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def add_guest(db, values):
    print("\n\n\n\nin insert guest function\n\n\n\n")
    insert = 'insert into Client value ( \''
    values['name'] = values['name'].replace('\'', '\\\'')
    value = []
    for val in values:
        value.append(values[val])
    insert = insert + '\',\''.join(value) + '\' )'
    print(insert)
    cursor = db.cursor()
    try:
        cursor.execute(insert)
        information = cursor.fetchall()
        cursor.connection.commit()
        error = 0
        return information, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        error = 1
        return e, error

def search_all_account(db):
    search_all = 'select Client.Client_ID, Client.name, Account.bank_name, '
    search_all = search_all + 'Account.account_id, Account.balance, Account.count_type '
    search_all = search_all + 'from Client, Account, Client_Account '
    search_all = search_all + 'where Client.Client_ID = Client_Account.Client_ID '
    search_all = search_all + 'and Account.account_id = Client_Account.account_id '
    cursor = db.cursor()
    cursor.execute(search_all)
    info = cursor.fetchall()
    return info

def search_account(db, values):
    client_filter = {}
    account_filter = {}
    cursor = db.cursor()
    cursor.execute('desc Client')
    Client_attributes = cursor.fetchall()
    for item in Client_attributes:
        client_filter[item[0]] = values[item[0]]
    cursor.execute('desc Account')
    Account_attributes = cursor.fetchall()
    for item in Account_attributes:
        account_filter[item[0]] = values[item[0]]
    print(client_filter)
    print(account_filter)
    try:
        account_search = 'select Client.Client_ID, Client.name, Account.bank_name, '
        account_search = account_search + 'Account.account_id, Account.balance, Account.count_type '
        account_search = account_search + 'from Client, Account, Client_Account '
        account_search = account_search + 'where Client.Client_ID = Client_Account.Client_ID '
        account_search = account_search + 'and Account.account_id = Client_Account.account_id '
        for key in client_filter:
            if(client_filter[key] != ''):
                account_search = account_search + ' and Client.' + str(key) + ' like \'%' + client_filter[key] + '%\' '
        for key in account_filter:
            if(account_filter[key] != ''):
                account_search = account_search + ' and Account.' + str(key) + ' like \'%' + account_filter[key] + '%\' '
        print(account_search)
        cursor.execute(account_search)
        info = cursor.fetchall()
        print(info)
        error = 0
        return info, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        error = 1
        return e, error

def add_saving_account(db, values):
    Client_ID = values['Client_ID']
    bank_name = values['bank_name']
    account_id = values['account_id']
    balance = float(values['balance'])
    open_date = datetime.datetime.now().strftime("%Y-%m-%d")
    recent_visit_date = datetime.datetime.now().strftime("%Y-%m-%d")
    count_type = 0
    interest_rate = float(values['interest_rate'])
    currency_type = values['currency_type']
    try:
        cursor = db.cursor()
        check_client_exist = 'select count(*) from Client where Client_ID = \'' + Client_ID + '\''
        cursor.execute(check_client_exist)
        client_exist = cursor.fetchall()
        if client_exist[0][0] == 0:
            error = 1
            return 'Client not exist', error
        check_account_exist = 'select count(*) from Account where account_id = \'' + account_id + '\''
        cursor.execute(check_account_exist)
        account_exist = cursor.fetchall()
        print(account_exist[0][0])
        if account_exist[0][0] == 0:
            account_insert = 'insert into Account value ('
            account_insert = account_insert + '\'' + bank_name + '\', '
            account_insert = account_insert + '\'' + account_id + '\', '
            account_insert = account_insert + str(balance) + ', '
            account_insert = account_insert + '\'' + open_date + '\', '
            account_insert = account_insert + '\'' + recent_visit_date + '\', '
            account_insert = account_insert + str(count_type) + ') '
            print(account_insert)
            cursor.execute(account_insert)
            saving_account_insert = 'insert into saving_account value (\'' + account_id + '\', '
            saving_account_insert = saving_account_insert + str(interest_rate) + ', '
            saving_account_insert = saving_account_insert + '\'' + currency_type + '\')'
            print(saving_account_insert)
            cursor.execute(saving_account_insert)
        client_own_account = 'insert into Client_Owns_Saving_Account value (\'' + Client_ID + '\', '
        client_own_account = client_own_account + '\'' + bank_name + '\')'
        print(client_own_account)
        cursor.execute(client_own_account)
        client_account_insert = 'insert into Client_Account value ('
        client_account_insert = client_account_insert + '\'' + account_id + '\', '
        client_account_insert = client_account_insert + '\'' + Client_ID + '\')'
        cursor.execute(client_account_insert)
        cursor.connection.commit()
        print(client_account_insert)
        logfile = 'insert into logfile value (\'' + bank_name + '\', \'' + open_date + '\', 0, \'' + str(balance) + '\', 1)'
        cursor.execute(logfile)
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        error = 1
        return e, error

def add_checking_account(db, values):
    Client_ID = values['Client_ID']
    bank_name = values['bank_name']
    account_id = values['account_id']
    balance = float(values['balance'])
    open_date = datetime.datetime.now().strftime("%Y-%m-%d")
    recent_visit_date = datetime.datetime.now().strftime("%Y-%m-%d")
    count_type = 1
    over_draft = float(values['over_draft'])
    try:
        cursor = db.cursor()
        check_client_exist = 'select count(*) from Client where Client_ID = \'' + Client_ID + '\''
        cursor.execute(check_client_exist)
        client_exist = cursor.fetchall()
        if client_exist[0][0] == 0:
            error = 1
            return 'Client not exist', error
        check_account_exist = 'select count(*) from Account where account_id = \'' + account_id + '\''
        cursor.execute(check_account_exist)
        account_exist = cursor.fetchall()
        print(account_exist[0][0])
        if account_exist[0][0] == 0:
            account_insert = 'insert into Account value ('
            account_insert = account_insert + '\'' + bank_name + '\', '
            account_insert = account_insert + '\'' + account_id + '\', '
            account_insert = account_insert + str(balance) + ', '
            account_insert = account_insert + '\'' + open_date + '\', '
            account_insert = account_insert + '\'' + recent_visit_date + '\', '
            account_insert = account_insert + str(count_type) + ') '
            print(account_insert)
            cursor.execute(account_insert)
            checking_account_insert = 'insert into checking_account value (\'' + account_id + '\', '
            checking_account_insert = checking_account_insert + str(over_draft) + ')'
            print(checking_account_insert)
            cursor.execute(checking_account_insert)
        client_own_account = 'insert into Client_Owns_Checking_Account value (\'' + Client_ID + '\', '
        client_own_account = client_own_account + '\'' + bank_name + '\')'
        print(client_own_account)
        cursor.execute(client_own_account)
        client_account_insert = 'insert into Client_Account value ('
        client_account_insert = client_account_insert + '\'' + account_id + '\', '
        client_account_insert = client_account_insert + '\'' + Client_ID + '\')'
        cursor.execute(client_account_insert)
        cursor.connection.commit()
        print(client_account_insert)
        logfile = 'insert into logfile value (\'' + bank_name + '\', \'' + open_date + '\', 0, \'' + str(balance) + '\', 1)'
        cursor.execute(logfile)
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        error = 1
        return e, error

def delete_saving_account(db, values):
    Client_ID = values['Client_ID']
    bank_name = values['bank_name']
    account_id = values['account_id']
    cursor = db.cursor()
    try:
        delete_from_own_account = 'delete from Client_Owns_Saving_Account where Client_ID = \'' + Client_ID + '\''
        delete_from_own_account = delete_from_own_account + ' and bank_name = \'' + bank_name + '\''
        print(delete_from_own_account)
        cursor.execute(delete_from_own_account)
        delete_from_client_account = 'delete from Client_Account where account_id = \'' + account_id + '\''
        delete_from_client_account = delete_from_client_account + ' and Client_ID = \'' + Client_ID + '\''
        print(delete_from_client_account)
        cursor.execute(delete_from_client_account)
        check_user_num = 'select count(*) from Client_Account where account_id = \'' + account_id + '\''
        print(check_user_num)
        cursor.execute(check_user_num)
        user_num = cursor.fetchall()
        if user_num[0][0] == 0:
            delete_from_saving_account = 'delete from saving_account where account_id = \'' + account_id + '\''
            print(delete_from_saving_account)
            cursor.execute(delete_from_saving_account)
            delete_account = 'delete from Account where account_id = \'' + account_id + '\''
            print(delete_account)
            cursor.execute(delete_account)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        logfile = 'insert into logfile value (\'' + bank_name + '\', \'' + date + '\', 0, 0, 1)'
        cursor.execute(logfile)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def delete_checking_account(db, values):
    Client_ID = values['Client_ID']
    bank_name = values['bank_name']
    account_id = values['account_id']
    cursor = db.cursor()
    try:
        delete_from_own_account = 'delete from Client_Owns_Checking_Account where Client_ID = \'' + Client_ID + '\''
        delete_from_own_account = delete_from_own_account + ' and bank_name = \'' + bank_name + '\''
        print(delete_from_own_account)
        cursor.execute(delete_from_own_account)
        delete_from_client_account = 'delete from Client_Account where account_id = \'' + account_id + '\''
        delete_from_client_account = delete_from_client_account + ' and Client_ID = \'' + Client_ID + '\''
        print(delete_from_client_account)
        cursor.execute(delete_from_client_account)
        check_user_num = 'select count(*) from Client_Account where account_id = \'' + account_id + '\''
        print(check_user_num)
        cursor.execute(check_user_num)
        user_num = cursor.fetchall()
        if user_num[0][0] == 0:
            delete_from_checking_account = 'delete from checking_account where account_id = \'' + account_id + '\''
            print(delete_from_checking_account)
            cursor.execute(delete_from_checking_account)
            delete_account = 'delete from Account where account_id = \'' + account_id + '\''
            cursor.execute(delete_account)
            print(delete_account)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        logfile = 'insert into logfile value (\'' + bank_name + '\', \'' + date + '\', 0, 0, 1)'
        print(logfile)
        cursor.execute(logfile)
        print(logfile)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def search_saving_account(db, values):
    account_id = values['account_id']
    select_account = 'select * from saving_account where account_id = \'' + account_id + '\''
    try:
        cursor = db.cursor()
        cursor.execute(select_account)
        info = cursor.fetchall()
        error = 0
        return info, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def search_checking_account(db, values):
    account_id = values['account_id']
    select_account = 'select * from checking_account where account_id = \'' + account_id + '\''
    try:
        cursor = db.cursor()
        cursor.execute(select_account)
        info = cursor.fetchall()
        error = 0
        return info, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def update_saving_account(db, values, pre_values):
    Client_ID = values['Client_ID']
    account_id = values['account_id']
    bank_name = values['bank_name']
    pre_bank_name = pre_values['bank_name']
    balance = values['balance']
    pre_balance = pre_values['balance']
    interest_rate = values['interest_rate']
    currency_type = values['currency_type']
    recent_visit_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor = db.cursor()
    try:
        if(bank_name != pre_bank_name):
            update_own_account = 'update Client_Owns_Saving_Account set bank_name = \'' + bank_name + '\''
            update_own_account = update_own_account + ' where Client_ID = \'' + Client_ID + '\''
            print(update_own_account)
            cursor.execute(update_own_account)
        update_saving = 'update saving_account set interest_rate = ' + str(interest_rate)
        update_saving = update_saving + ', currency_type = \'' + currency_type + '\''
        update_saving = update_saving + ' where account_id = \'' + account_id + '\''
        print(update_saving)
        cursor.execute(update_saving)
        update_account = 'update Account set bank_name = \'' + bank_name + '\''
        update_account = update_account + ', balance = ' + str(balance)
        update_account = update_account + ', recent_visit_date = \'' + recent_visit_date + '\''
        update_account = update_account + ' where account_id = \'' + account_id + '\''
        print(update_account)
        cursor.execute(update_account)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        logfile = 'insert into logfile value (\'' + bank_name + '\', \'' + date + '\', 0,\'' + str(float(balance) - float(pre_balance)) + '\', 1)'
        print(logfile)
        cursor.execute(logfile)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def update_checking_account(db, values, pre_values):
    Client_ID = values['Client_ID']
    account_id = values['account_id']
    bank_name = values['bank_name']
    pre_bank_name = pre_values['bank_name']
    balance = values['balance']
    pre_balance = pre_values['balance']
    over_draft = values['over_draft']
    recent_visit_date = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor = db.cursor()
    try:
        if(bank_name != pre_bank_name):
            update_own_account = 'update Client_Owns_Checking_Account set bank_name = \'' + bank_name + '\''
            update_own_account = update_own_account + ' where Client_ID = \'' + Client_ID + '\''
            print(update_own_account)
            cursor.execute(update_own_account)
        update_checking = 'update checking_account set over_draft = ' + str(over_draft)
        update_checking = update_checking + ' where account_id = \'' + account_id + '\''
        print(update_checking)
        cursor.execute(update_checking)
        update_account = 'update Account set bank_name = \'' + bank_name + '\''
        update_account = update_account + ', balance = ' + str(balance)
        update_account = update_account + ', recent_visit_date = \'' + recent_visit_date + '\''
        update_account = update_account + ' where account_id = \'' + account_id + '\''
        print(update_account)
        cursor.execute(update_account)
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        logfile = 'insert into logfile value (\'' + bank_name + '\', \'' + date + '\', 0,\'' + str(float(balance) - float(pre_balance)) + '\', 1)'
        print(logfile)
        cursor.execute(logfile)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def get_account_detail(db, values):
    account_id = values['account_id']
    count_type = values['count_type']
    try:
        cursor = db.cursor()
        if(count_type == 0):
            get_saving_detail = 'select * from Account, saving_account where Account.account_id = saving_account.account_id'
            get_saving_detail = get_saving_detail + ' and Account.account_id = \'' + account_id + '\''
            cursor.execute(get_saving_detail)
            print(get_saving_detail)
            info = cursor.fetchall()
        else:
            get_checking_detail = 'select * from Account, checking_account where Account.account_id = checking_account.account_id'
            get_checking_detail = get_checking_detail + ' and Account.account_id = \'' + account_id + '\''
            cursor.execute(get_checking_detail)
            print(get_checking_detail)
            info = cursor.fetchall()
        print(info)
        error = 0
        return info[0], error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def add_loan(db, values):
    Loan_ID = values['Loan_ID']
    bank_name = values['bank_name']
    Loan_Amount = values['Loan_Amount']
    try:
        cursor = db.cursor()
        loan_insert = 'insert into Loan value (\'' + Loan_ID + '\', \'' + bank_name + '\', \'' + str(Loan_Amount) + '\')'
        cursor.execute(loan_insert)
        print(loan_insert)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def search_start_loan(db):
    search_loan = 'select tb2.Loan_ID, tb2.bank_name, tb2.Loan_Amount, tb1.total_Amount '
    search_loan = search_loan +  'from (select Loan_ID, sum(Pay_Amount) as total_Amount from Pay_Loan group by Loan_ID ) tb1, Loan tb2'
    search_loan = search_loan + ' where tb1.Loan_ID = tb2.Loan_ID'
    cursor = db.cursor()
    cursor.execute(search_loan)
    info = cursor.fetchall()
    return info

def search_not_start_loan(db):
    search_loan = 'select * from Loan where Loan.Loan_ID not in (select Loan_ID from Pay_Loan)'
    cursor = db.cursor()
    cursor.execute(search_loan)
    info = cursor.fetchall()
    return info

def search_start_loan_condition(db, values):
    search_loan = 'select tb2.Loan_ID, tb2.bank_name, tb2.Loan_Amount, tb1.total_Amount '
    search_loan = search_loan +  'from (select Loan_ID, sum(Pay_Amount) as total_Amount from Pay_Loan group by Loan_ID ) tb1, Loan tb2'
    search_loan = search_loan + ' where tb1.Loan_ID = tb2.Loan_ID'
    Loan_ID = values['Loan_ID']
    bank_name = values['bank_name']
    Loan_Amount = values['Loan_Amount']
    if(Loan_ID != ''):
        search_loan = search_loan + ' and tb2.Loan_ID like \'%' + Loan_ID + '%\''
    if(bank_name != ''):
        search_loan = search_loan + ' and tb2.bank_name like \'%' + bank_name + '%\''
    if(Loan_Amount != ''):
        search_loan = search_loan + ' and tb2.Loan_Amount = ' + str(Loan_Amount) + '\''
    print(search_loan)
    cursor = db.cursor()
    cursor.execute(search_loan)
    info = cursor.fetchall()
    return info

def search_not_start_loan_condition(db, values):
    search_loan = 'select * from Loan where Loan.Loan_ID not in (select Loan_ID from Pay_Loan)'
    Loan_ID = values['Loan_ID']
    bank_name = values['bank_name']
    Loan_Amount = values['Loan_Amount']
    if(Loan_ID != ''):
        search_loan = search_loan + ' and Loan_ID like \'%' + Loan_ID + '%\''
    if(bank_name != ''):
        search_loan = search_loan + ' and bank_name like \'%' + bank_name + '%\''
    if(Loan_Amount != ''):
        search_loan = search_loan + ' and Loan_Amount = ' + str(Loan_Amount) + '\''
    cursor = db.cursor()
    cursor.execute(search_loan)
    info = cursor.fetchall()
    return info

def add_pay_loan(db, values):
    Pay_Code = values['Pay_Code']
    Loan_ID = values['Loan_ID']
    Client_ID = values['Client_ID']
    Pay_Amount = values['Pay_Amount']
    Pay_Day = datetime.datetime.now().strftime("%Y-%m-%d")
    check_paid_amount = 'select sum(Pay_Amount) from Pay_Loan where Loan_ID = \'' + Loan_ID + '\''
    check_total_amount = 'select Loan_Amount from Loan where Loan_ID = \'' + Loan_ID + '\''
    try:
        cursor = db.cursor()
        cursor.execute(check_paid_amount)
        temp = cursor.fetchall()
        paid_amount = temp[0][0]
        if(paid_amount == None):
            paid_amount = 0
        cursor.execute(check_total_amount)
        temp = cursor.fetchall()
        total_amount = temp[0][0]
        if(total_amount < paid_amount + float(Pay_Amount)):
            error = 1
            return 'Pay Amount exceed Loan Amount !', error
        insert_pay_loan = 'insert into Pay_Loan value (\'' + Pay_Code + '\', \'' + Loan_ID + '\', \''
        insert_pay_loan = insert_pay_loan + Client_ID + '\', ' + str(Pay_Amount) + ', \'' + Pay_Day + '\')'
        print(insert_pay_loan)
        cursor.execute(insert_pay_loan)
        get_bank_name = 'select bank_name from Loan where Loan_ID = \'' + Loan_ID + '\''
        cursor.execute(get_bank_name)
        info = cursor.fetchall()
        bank_name = info[0][0]
        logfile = 'insert into logfile value (\'' + bank_name + '\', \'' + Pay_Day + '\', 1, ' + str(Pay_Amount) + ', 1)'
        print(logfile)
        cursor.execute(logfile)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def get_loan_detail(db, values):
    Loan_ID = values['Loan_ID']
    loan_detail = 'select Pay_Code, Client.Client_ID, Pay_Amount, date_format(Pay_Day, \'%Y-%m-%d \'), name, tel from Pay_Loan, Client where Pay_Loan.Client_ID = Client.CLient_ID'
    loan_detail = loan_detail + ' and Pay_Loan.Loan_ID = \'' + Loan_ID + '\''
    cursor = db.cursor()
    cursor.execute(loan_detail)
    info = cursor.fetchall()
    print(loan_detail)
    print(info)
    return info

def delete_loan(db, values):
    Loan_ID = values['Loan_ID']
    pay_loan_delete = 'delete from Pay_Loan where Loan_ID = \'' + Loan_ID + '\''
    loan_delete = 'delete from Loan where Loan_ID = \'' + Loan_ID + '\''
    try:
        cursor = db.cursor()
        cursor.execute(pay_loan_delete)
        cursor.execute(loan_delete)
        cursor.connection.commit()
        error = 0
        return None, error
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        error = 1
        return e, error

def get_logfile(db):
    cursor = db.cursor()
    get_info = 'select * from logfile'
    cursor.execute(get_info)
    info = cursor.fetchall()
    return info

def get_saving_by_bank_name(db, bank_name):
    cursor = db.cursor()
    get_info = 'select * from logfile where type = 0 and bank_name = \'' + bank_name + '\''
    cursor.execute(get_info)
    info = cursor.fetchall()
    return info

def get_loan_by_bank_name(db, bank_name):
    cursor = db.cursor()
    get_info = 'select * from logfile where type = 1 and bank_name = \'' + bank_name + '\''
    cursor.execute(get_info)
    info = cursor.fetchall()
    print(get_info)
    print(info)
    return info

def db_close(db):
    if db is not None:
        db.close()

if __name__ == "__main__":
    db = db_login("root", "457213", "127.0.0.1", "bank_system")

    search_guest(db, {})

    # tabs = db_showtable(db)
    
    db_close(db)