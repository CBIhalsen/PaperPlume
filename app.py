from flask import Flask, render_template, request, redirect, url_for,  jsonify,make_response, send_from_directory
import asyncio
import json
import pytz
from decimal import Decimal
import requests
import threading
from alipay import AliPay
import stripe
import yaml
from datetime import datetime, timedelta
from cut_text import split_and_trim_text
import urllib.parse
from de_encrypt import AESCipher
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
# twistd -n web --wsgi app.app
from waitress import serve
from flaskext.mysql import MySQL
from flask_cors import CORS
import base_table as vsql
from session_fake import chat
from payment import receiver_payment
from sub import process_outline, create_word

from verify_email import generate_verification_code,SendMail

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

import time
app = Flask(__name__,template_folder='templates')
CORS(app)
# login_manager = LoginManager(app)

app.config['SECRET_KEY'] = 'your-secret-key'
# mysql = MySQL()

app.config['JWT_SECRET_KEY'] = 'verseed'  # 设置JWT密钥，请使用与前端相同的密钥
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 7 * 24 * 60 * 60  # 设置令牌的过期时间为7天
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'  # MySQL 主机地址
# app.config['MYSQL_DATABASE_PORT'] = 3306  # MySQL 端口号
# app.config['MYSQL_DATABASE_USER'] = 'root'  # MySQL 用户名
# app.config['MYSQL_DATABASE_PASSWORD'] = 'abc123'  # MySQL 密码
# app.config['MYSQL_DATABASE_DB'] = 'paper'  # MySQL 数据库名
# mysql.init_app(app)
jwt = JWTManager(app)
#
# chat_history = []
paper_name = []
# 配置静态文件的路由
# @app.route('/static/<path:styles.css>')
# def static_files(filename):
#     return app.send_static_file(filename)
# class User:
#     def __init__(self, id,password):
#         self.id = id
#         self.password = password
# 全局字典来存储数据
global_dict = {}


# SQLAlchemy URI格式：dialect+driver://username:password@host:port/database
DATABASE_URI = 'mysql+pymysql://root:abc123@localhost:3306/paper'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def remove_expired_items():
    current_time = datetime.datetime.now()
    keys_to_remove = []

    for key, value in global_dict.items():
        if 'expire_at' in value and value['expire_at'] < current_time:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        del global_dict[key]

    # 重新设定定时器
    threading.Timer(60.0, remove_expired_items).start()



    # temperature=0.7,
    #         max_tokens=1300,


def get_exchange_rates():
    url = "https://v6.exchangerate-api.com/v6/28381c944398a8cb4a505275/latest/USD"
    response = requests.get(url)
    data = response.json()
    exchange_rates = data['conversion_rates']['CNY']

    with open('./config/currency.yaml', 'r', encoding='utf-8') as infile:
        CNY = yaml.safe_load(infile)['USD-CNY']
    currency = {'USD-CNY': exchange_rates, 'Y-USD-CNY': CNY}

    with open('./config/currency.yaml', 'w', encoding='utf-8') as file:
        yaml.dump(currency, file)
        # json.dump(currency, file)
    threading.Timer(24*60*60.0, get_exchange_rates).start()
    num_str = data['conversion_rates']['CNY']

    num = float(num_str)
    rounded_num = round(num, 2) + 0.01
    rounded_num = round(rounded_num, 2)
    # print(rounded_num)
    # print(data)

    return data




@app.route("/")
def index():
    return render_template("papge.html")


@app.route('/check',methods=['GET'])
def check():
    Email = request.args.get('email')
    type = request.args.get('type')
    print(Email,'check email')
    session = Session()
    verify = session.query(vsql.Email).filter_by(email=Email).first()
    if verify:
        value = verify.exist
# exist= 1 三方绑定已存在
    session.close()
    if type=='register':

        if verify and value:

            return "False"

        else:

            return "True"
    else:
        if verify:
            return "True"
        else:
            return "none"



@app.route("/user_information", methods=["POST"])
@jwt_required()
def user_information():
    current_user = get_jwt_identity()
    user_id = current_user
    session = Session()
    print(user_id)
    verify = session.query(vsql.User).filter_by(id=user_id).first()

    number = verify.Number
    # session['id'] = user[0]
    Token = verify.tokens
    EmailStr= verify.Email
    balance = verify.Balance
    return jsonify({'message': 'success', 'userid': user_id, "number": number, "Email": EmailStr,
                    "Token": Token,"balance":balance})

@app.route('/login', methods=['POST'])
def login():
    # data = request.get_json()
    data = json.loads(request.data)
    EmailStr = data['Email']
    password = data['password']

    # print(EmailStr, password)

    # conn = mysql.connect()
    # cursor = conn.cursor()
    #
    session = Session()
    verify = session.query(vsql.User).filter_by(Email=EmailStr).first()
    session.close()

    # # 验证用户名是否存在
    # cursor.execute("SELECT * FROM users WHERE Email = %s", (Email,))
    #
    # user = cursor.fetchone()
    if not verify:
        # print("不存在")
        # print(jsonify({'message': '用户名不存在'}))
        return jsonify({'message': 'Email不存在'})

    # 验证用户名和密码是否正确
    # cursor.execute("SELECT * FROM users WHERE Email = %s AND password = %s", (Email, password))
    # user = cursor.fetchone()
    user = session.query(vsql.User).filter_by(Email=EmailStr,password=password).first()
    session.close()
    # cursor.execute("SELECT * FROM users WHERE Email = %s ", (Email))
    # verify = cursor.fetchone()
    # print("user:",user)
    # print(verify)
    # print(len(verify.password))

    if user and len(verify.password) != 0:
        # session['Email'] = Email  # 将用户名存储到 session 中
        # session['password'] = password  # 将密码存储到 session 中
        # session['Token']  = user[3]
        # session['username'] = user[1]

        number = user.Number
        # session['id'] = user[0]
        Token = user.tokens
        # print("session:",session)
        # print(user.username)
        # print("tokens:",user.tokens)
        # print("成功")
        access_token = create_access_token(identity=user.id)

        return jsonify({'message': '登录成功', "password": password, "number": number, "Email": EmailStr,
                        "Token": Token, "access_token": access_token})
    elif not user and len(verify.password) == 0:
        # print(0)
        return jsonify({'message': 'not'})

    else:
        return jsonify({'message': 'perror'})
    print("password error")




@app.route('/loginout')
def loginout():

    return 200


@app.route("/generate_outline", methods=["POST"])
@jwt_required()
def generate_outline():
    url = request.host_url
    # print("url",url)
    # 获取JWT令牌中的用户身份
    current_user = get_jwt_identity()
    user_id = current_user
    if current_user:
        print("jwt:", user_id)
        data = json.loads(request.data)
        # EmailStr = data['Email']
        # password = data['password']
        text = data.get('reference')

        # print("reference",text)
        style = data['style']

        language = data['language']
        title = data.get('title')
        model = data['model']
        n = 1
        if model == 'gpt-4':
            n = 25
        else :
            n = 1
        print(model)
        if title == "":
            return "Please input the title"
        # print("style:",style,"language:",language,"model:",model)
        # print("len text",len(text))
        session = Session()
        verify = session.query(vsql.User).filter_by(id=user_id).first()
        balance =verify.Balance
        if balance<0:
            return jsonify({'type': 'refuse'})

        if len(text)==0:
            reference = None
            summary_tokens = 0
            if language == 'zh-CN':
                first_input = "生成一个关于「{}」的论文大纲。注意:二级标题由汉字开头,次级标题开头必须是空格!  ".format(title)
            elif language == 'zh_TW':
                first_input = " 生成一個關於「{}」的論文大綱。注意:一級標題由漢字開頭,次級標題開頭必須是空格!  ".format(title)
            elif language == 'ja':
                first_input = "Generate a paper outline on the '{}' .Note: The subheading must begin with a space, Use Japanese! ".format(title)
            else :
                first_input = "Generate a paper outline on the '{}' .Note: The subheading must begin with a space!!  ".format(title)
            test = []
        elif len(text) !=0:
            reference,summary_tokens = split_and_trim_text(text)
            if language == 'zh':
                first_input = "生成一个关于「{}」的论文大纲,参考资料包括（{}）。注意:一级标题由汉字开头,次级标题开头必须是空格!  ".format(title, reference)
            elif language == 'zh_tc':
                first_input = " 生成一個關於「{}」的論文大綱，參考資料包括（{}）。注意:一级标题由汉字开头,次级标题开头必须是空格!  ".format(title, reference)
            elif language == 'ja':
                first_input = "Generate a paper outline on the '{}' with references ({}).Note: The subheading must begin with a space, Use Japanese! ".format(title,reference)
            else:
                first_input = "Generate a paper outline on the '{}' with references ({}).Note: The subheading must begin with a space!!  ".format(title,reference )
            test = []

        global paper_name
        paper_name.append(title)
        # print(style)
        # print(language)
        # print("paper_name:", paper_name)
        # print(title)
        #
        # print(title)
        # first_input = "根据论文:{},列出详细的结构化提纲。注意:一级标题由汉字开头,次级标题开头必须是空格!  下面是提纲的参考资料:{}".format(title,reference)

        outline_history = []
        receive_history = []

        # while True:
        #     try:
        First_reply, total_tokens = chat(language,style,reference,model=model).first_chat(prompt=first_input, title=title, history=outline_history)
            #     break  # 如果没有发生错误，则跳出循环
            # except Exception as e:
            #     print(f"Error occurred: {e}")
            #     print("Retrying...")

        # test.append(First_reply)
        # print("test:", test)
        # print(First_reply)

        # 直接执行更新操作并更新token和balance值
        total_tokens = total_tokens +summary_tokens
        print('总token',total_tokens)

        balance_value = Decimal(str(total_tokens / 1000 * 0.002 *n))

        verify.tokens += total_tokens
        verify.Balance -= balance_value

        # document.title = 'Updated Title'
        session.commit()
        session.close()


        # print("total_tokens:", total_tokens)
        return jsonify({'message': First_reply,'type':'success'})
        # return First_reply
    else:
        return jsonify({'type': 'refuse'})



@app.route("/write_docx", methods=["POST"])
@jwt_required()
def write_docx():
    total_tokens = 0
    # 获取JWT令牌中的用户身份
    current_user = get_jwt_identity()
    user_id = current_user
    if current_user:
        # print("jwt:", user_id)
        nummber =0
        # chat_history=[]
        outline = request.form.get("first_reply")
        # print("outline:",outline)
        timestamp = request.form.get("timestamp")
        title = request.form.get("title")
        if title == "":
            title = "unname"
        style = request.form.get("style")
        language = request.form.get("language")
        model = request.form.get("model")
        # print('model',model)

        session = Session()

        verify = session.query(vsql.User).filter_by(id=user_id).first()
        balance =verify.Balance
        n =1
        if model == 'gpt-4':
            n=25
        elif model== 'gpt-3.5-turbo':
            n=1
        elif model=='gpt-4'and balance<10:
            # print('refuse4')
            return 'refuse4'
        elif model=='gpt-3.5-turbo'and balance<0.5:
            return 'refuse3'

        documtns = vsql.documents(user_id=user_id,title=title,create_at=timestamp)
        session.add(documtns)
        session.commit()

        order_id = documtns.order_id


        temp = str(order_id)
        # print(temp)
        encrypted_title= str(AESCipher().encrypt(temp))+title
        # print("encrypted_title:",encrypted_title)

        create_word(encrypted_name=encrypted_title,language=language)



        btime =time.time()

        # print("大纲:",outline)
        start_time = time.time()

        total_tokens = process_outline(language=language,style=style,title=title,model=model).spilt(outline_str=outline,encrypted=encrypted_title)



        balance_value = 0.25 + total_tokens / 1000 * 0.002 * n

        verify.tokens += total_tokens
        verify.Balance -= Decimal(balance_value)
        verify.Number +=1


        url = encrypted_title+".docx"
        document = session.query(vsql.documents).filter_by(order_id=order_id).first()
        document.url =url
        document.Usage =balance_value
        document.states = 1
        session.commit()
        session.close()

        end_time=time.time()
        run_time = end_time - start_time
        url ="{}{}{}{}".format(request.host_url,'download/',encrypted_title,".docx")
        # print("共运行:",run_time)
        return url
    else:
        return jsonify({'message': 'No login'})
@app.route('/select_informaiton', methods=['GET'])
@jwt_required()
def select_information():
    current_user = get_jwt_identity()
    uid = current_user

    page = int(request.args.get('page'))

    size = int(request.args.get('per_page'))

    offset = (page - 1) * size
    # 验证用户名是否存在
    session = Session()
    total = session.query(vsql.documents).filter_by(user_id = uid).count()


    result = session.query(vsql.documents).filter_by(user_id = uid).order_by(vsql.documents.order_id.desc()).limit(size).offset(offset).all()

    session.close()


    if not result:
        # print("不存在")
        # print(jsonify({'message': '用户名不存在'}))
        return jsonify({'message': 'Email不存在'})

    session.close()
    # cursor.close()
    #
    # conn.close()
    # print(result)
    # 构建返回给前端的数据字典列表
    data = []
    for row in result:
        item = {
            'order_id': row.order_id,
            'title': row.title,
            'url': row.url,
            'create_at': row.create_at,
            'status': row.states,
            'Usage':row.Usage,
            'total': total

        }
        data.append(item)

    return jsonify(data)


@app.route('/download/<filename>')
def download(filename):
    directory = "../documents/word/users/"

    # 检查文件是否存在
    if os.path.exists(os.path.join(directory, filename)):
        response = make_response(send_from_directory(directory, filename, as_attachment=True))
        # print(filename)

        # 以'=='为分割点，提取文件名部分
        # file_name = filename.split("=='")[-1]

        # 去除文件扩展名，获取目标文本
        target_text = filename.split("==")[-1].split('.docx')[0]
        # print(target_text)


        new_filename = "{}.docx".format(target_text)

        # 对文件名进行URL编码
        encoded_filename = urllib.parse.quote(new_filename)

        # 设置Content-Disposition响应头
        response.headers["Content-Disposition"] = f"attachment; filename*=UTF-8''{encoded_filename}"

        return response
        # return send_from_directory(directory, filename, as_attachment=True,attachment_filename="zero.docx")
    else:
        return "文件不存在", 404


# 注册路由，接收用户输入的验证码和账号信息
@app.route('/register_account', methods=['POST'])
def register():
    temp_id = request.form.get('temp_id')
    user_code = request.form.get('code')
    print("验证码",user_code)
    # 从会话中获取验证码信息
    verification_code = global_dict.get(temp_id)
    print("register:",temp_id)
    print(global_dict )
    if verification_code and verification_code['code'] == user_code and verification_code['expire_at'] > pytz.utc.localize(datetime.now() ):


        type = request.form.get('type')
        password = request.form.get('password')
        email_str = request.form.get('email')
        print(email_str,password)
        # 假设使用MySQL扩展进行数据库操作



        session = Session()
        print('类型是',type)
        if type =='register':
            user = vsql.User(password=password, tokens=-2000, Email=email_str, Number=0, Balance=0.004)

            session.add(user)
            session.commit()
            user_id = user.id
            user_email = vsql.Email(email=email_str, exist=1,id=user_id)
            session.add(user_email)
            session.commit()

            # order_id = user.order_id
            session.close()
            print("success")
            return jsonify({'status':'success',"email":email_str,"password":password})
        else:
            verify = session.query(vsql.User).filter_by(Email=email_str).first()
            verify.password = password





            session.commit()

            # order_id = user.order_id
            session.close()
            print("success")
            return jsonify({'status':'success'})



    else:
        # 验证码不匹配或已过期，注册失败
        print("else")
        return jsonify({'status':'error'})

# 生成并发送验证码的路由
ip_requests = {}
@app.route('/send_code', methods=['POST'])
def send_verification_code():
    # data = request.get_json()
    # temp_id = request.form.get("reference")
    # text = request.form.get("reference")
    # style = request.form.get("style")
    # email_number = request.form.get('email')
    # print(temp_id)
    # email_number = '1421243966@qq.com'
    data = json.loads(request.data)
    email_number = data['email']
    temp_id = str(data['temp_id'])
    if not temp_id.isdigit() or len(temp_id) != 6:
        return "Illegal access"

    ip_address = request.remote_addr
    print("ip",ip_address)

    # 获取当前时间戳
    current_time = time.time()

    # 检查 IP 地址是否在字典中，且距离上次请求的时间是否超过 1 分钟
    if ip_address in ip_requests and current_time - ip_requests[ip_address]['timestamp'] <= 60:
        # 如果超过了请求次数限制，返回错误响应
        if ip_requests[ip_address]['count'] >= 2:
            return "Request limit exceeded"

        # 增加请求次数
        ip_requests[ip_address]['count'] += 1
    else:
        # 如果 IP 地址不在字典中或距离上次请求的时间超过 1 分钟，创建新的请求记录
        ip_requests[ip_address] = {'count': 1, 'timestamp': current_time}
    # email_number = request.form.get('email')

    # 生成验证码（示例中使用固定的验证码"1234"，实际情况应该是随机生成的）
    verification_code = generate_verification_code()

    # 获取当前时间
    current_time = datetime.now()
    current_time_aware = pytz.utc.localize(current_time)

    # 设置验证码的过期时间（当前时间往后推10分钟）
    expire_at = current_time_aware + timedelta(minutes=10)
    # 设置验证码的过期时间（示例中为当前时间往后推10分钟）
    # expire_at = current_time + timedelta(minutes=10)
    print("过期:",expire_at)
    print(global_dict )
    # 将验证码信息存储到会话中，使用用户ID作为会话键
    global_dict[temp_id] = {'code': verification_code, 'expire_at': expire_at}

    print(global_dict[temp_id])
    print(global_dict )
    # 发送验证码的逻辑，这里仅打印验证码，实际情况下可以通过短信、邮件等方式发送验证码
    SendMail(email_number,'Welcome to PaperPlume ! Begin your new journey!',verification_code)
    print(f"Verification code for user {temp_id}: {verification_code}")

    # 返回JSON响应
    return jsonify({'message': 'Verification code sent'})


@app.route('/api/auth/callback', methods=['POST'])
def auth_callback():
    # 获取前端发送的用户信息
    user_info = request.get_json()
    print(user_info)
    if not user_info:
        return jsonify({
            'status': 'error'
        })

    type =user_info.get('type')
    # username = user_info.get('name')
    Email = user_info.get('email')
    # conn = mysql.connect()
    # cursor = conn.cursor()
    thirdid = user_info.get('uid')
    access_token = user_info.get('token')
    # 执行插入数据的SQL语句

    if type == 'google':
        url = f'https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}'

        # 发送GET请求并获取响应
        response = requests.get(url)
        data = response.json()
        third_email = data.get('email')
        print(third_email)
        # 检查响应状态码
        if Email != third_email:
            # 解析JSON数据

            return jsonify({"status": "error"})

    else:
        # 构建URL
        url = 'https://api.github.com/user/emails'

        # 设置请求头部，包含Authorization信息
        headers = {
            'Authorization': f'token {access_token}'
        }

        # 发送GET请求并获取响应
        response = requests.get(url, headers=headers)

        # 检查响应状态码

        data = response.json()
        third_email = data[0].get('email')
        if Email != third_email:
            # 解析JSON数据
            return jsonify({"status": "error"})

    session = Session()
    # verify = session.query(vsql.User).filter_by(id=user_id).first()
    # verify.tokens += total_tokens
    # verify.Balance -= Decimal(balance_value)
    # verify.Number += 1


    # cursor.execute("SELECT * FROM email WHERE Email = %s", (Email,))
    # user = cursor.fetchone()
    user = session.query(vsql.Email).filter_by(email=Email).first()
    # print(user.exist,"exist值")
    if not user:
        if type == 'google':

            # insert_query = "INSERT INTO users (username, password, tokens, email, number, balance,google_id) VALUES (%s, %s, %s, %s, %s, %s,%s)"
            # values = (username, '', -2000, Email, 0, 0.004, thirdid)
            # cursor.execute(insert_query, values)
            userinformation = vsql.User(password='',tokens=-2000, Email=Email,google_id=thirdid,Number=0, Balance=0.004)
            session.add(userinformation)
            session.commit()
            user_id = userinformation.id
            print('新id',user_id)
            user_email = vsql.Email(id=user_id,email=Email)

            session.add(user_email)
            session.commit()

            # insert_email = "INSERT INTO email ( email) VALUES (%s)"
            # cursor.execute(insert_email, Email)
        else:
            userinformation = vsql.User(password='',tokens=-2000, Email=Email,github_id=thirdid,Number=0, Balance=0.004)
            session.add(userinformation)
            session.commit()
            user_id = userinformation.id
            print('新id', user_id)
            user_email = vsql.Email(id=user_id,email=Email)

            session.add(user_email)
            session.commit()


        session.close()

        access_token = create_access_token(identity=user_id)
        print(access_token)
        return jsonify({'message': '登录成功', "Email": Email, "access_token": access_token ,'status': 'success'})

    # 提交事务并关闭连接
    elif user and not user.exist:

        if type == 'google':

            verify = session.query(vsql.User).filter_by(Email=Email).first()
            verify.google_id = thirdid
            # verify.Balance -= Decimal(balance_value)
            # verify.Number += 1

            # update_query = "UPDATE users SET google_id = %s WHERE email = %s"
            # values = (thirdid,Email)
            # cursor.execute(update_query, values)
        else:
            verify = session.query(vsql.User).filter_by(Email=Email).first()
            verify.github_id = thirdid

            # update_query = "UPDATE users SET github_id = %s WHERE email = %s"
            # values = (thirdid,Email)
            # cursor.execute(update_query, values)

        session.commit()
        # conn.commit()
        # cursor.close()
        # conn.close()


        print(user.id)

        print("成功")
        access_token = create_access_token(identity=user.id)

        return jsonify({'message': '登录成功', "Email": Email, "access_token": access_token ,'status': 'success'})
    elif user and user.exist:

        if type == 'google':

            verify = session.query(vsql.User).filter_by(Email=Email).first()


        else:
            verify = session.query(vsql.User).filter_by(Email=Email).first()

        session.commit()
        # conn.commit()
        # cursor.close()
        # conn.close()


        print("id值",user.id)

        print("成功")
        access_token = create_access_token(identity=user.id)

        return jsonify({'message': '登录成功', "Email": Email, "access_token": access_token ,'status': 'success'})


    else:
        print('eror,cuo')
        return jsonify({
            'status': 'error fault'
        })
    # TODO: 处理用户信息,登录或注册用户

    # 返回结果
    # return jsonify({
    #     'status': 'success'
    # })



@app.route('/payment-notification', methods=['POST'])
def payment_notification():
    data = request.form.to_dict()  # 获取支付宝POST过来的通知数据
    signature = data.pop('sign')  # 提取签名
    # print('Received notification:', json.dumps(data, indent=4))
    with open("./config/alipay_private_key.pem", "r") as private_key_file:
        app_private_key_string = private_key_file.read()

    with open("./config/alipay_public_key.pem", "r") as public_key_file:
        alipay_public_key_string = public_key_file.read()
    #
    # appid="2021004101646681",
    alipay = AliPay(
        appid="2021004115697613",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=False,
    )

    success = alipay.verify(data, signature)
    if success:
        # 签名验证成功后，你可以更新你的订单状态

        out_trade_no = data["out_trade_no"]
        pairs = out_trade_no.split(",")

        for pair in pairs:
            key, value = pair.split("=")
            if key == "uid":
                uid = value
            elif key == "amount":
                amount = value

        if uid and amount:
            # print("UID:", uid)
            # print("Amount:", amount)
            session = Session()
            verify = session.query(vsql.User).filter_by(id=uid).first()
            verify.Balance += Decimal(amount)
            session.commit()
            session.close()

        else:
            print("UID and/or amount not found in 'out_trade_no'.")

        # print('Verified notification:', json.dumps(data, indent=4))
        # TODO: 在此处更新你的订单状态

        return 'success'  # 告诉支付宝我们已经成功处理了通知
    else:
        # 如果签名验证失败，那么这可能是一个伪造的通知
        print('Failed to verify notification:', json.dumps(data, indent=4))
        return 'failure'

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    with open('./config/stripe.yaml', 'r',encoding='utf-8') as config_file:
        config = yaml.safe_load(config_file)

    stripe.api_key = config['api_key']

    endpoint_secret = config['endpoint_secret']
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']


    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e
    # payment_intent = event['data']['object']
    # print(payment_intent)
    # Handle the event
    # print(event['type'])
    if event['type'] == 'checkout.session.async_payment_failed':
        checkout = event['data']['object']
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        checkout = event['data']['object']

    elif event['type'] == 'checkout.session.completed':
        checkout = event['data']['object']
        amount =  checkout['amount_total']
        uid = checkout['metadata']['user_uid']
        # print('id',uid,'amout',amount)
        add_balance = Decimal(amount) / 100
        session = Session()
        verify = session.query(vsql.User).filter_by(id=uid).first()
        verify.Balance +=add_balance
        session.commit()
        session.close()
    elif event['type'] == 'checkout.session.expired':
        checkout = event['data']['object']
    # ... handle other event types
    else:
        return 'error'
    # # print(checkout)
    # # print(checkout.get('metadata'))
    return jsonify(success=True)




@app.route('/create_payment', methods=['POST'])
@jwt_required()
def create_payment():
    uid = get_jwt_identity()
    data = request.get_json()
    type = data.get('type')
    print(type)
    amount = data.get('amount')
    trade_number=0
    if type =='alipay':
        session = Session()

        trade_nu = vsql.trade_number(amount=amount,uid=uid,create_at=datetime.now())

        session.add(trade_nu)
        session.commit()

        trade_number=trade_nu.number
        session.close()


    # 获取指定键的值

    url =  receiver_payment(type=type,amount=amount,uid=uid,trade_number=trade_number).payment()
    print(url)
    return jsonify({"type": type, "url": url})


@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()

    list1 = data['chatMessages']
    list2 = data['userMessages']
    prompt = data['prompt']
    # print(list2,"l2user")
    # print(list1,"l1sys")
    response_message , tokens = chat().normal_chat(prompt=prompt,user_message=list2,assistant_message=list1)
    # print(response_message)
    return jsonify({"sender": "service", "message": response_message})
#
# get_exchange_rates()
if __name__ == '__main__':
    # app.run()
    # app.run(host="127.0.0.1", port="8080")
    # app.run(host='localhost', port=8080, threaded=False, processes=1)

    get_exchange_rates()
    remove_expired_items()  # 开始定时器
    serve(app, host='0.0.0.0', port=8080)

    # app.run(debug=False,threaded=True,host='0.0.0.0', port=5000)
# b'LcSlFUg0io0CTACXKGK/tg=='论如何创造性打出“泉城济南”新名片.docx"
# b'CzBIcmG4lSLF8PiOCJbbAQ=='论如何创造性打出“泉城济南”新名片.docx