# -*- coding:utf-8 -*-
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

import secrets

def generate_verification_code():
    code = str(secrets.randbelow(900000) + 100000)  # 生成一个6位的随机数字验证码
    print(code)
    return code






def SendMail(to_email, title,number):
    EMAIL_FROM = 'xxx'  # 刚才配置的发信地址
    EMAIL_HOST_PASSWORD = "xxx"  # 密码
    # EMAIL_HOST, EMAIL_PORT = 'smtpdm.aliyun.com', 80
    # 自定义的回复地址

    # 构建alternative结构
    msg = MIMEMultipart('alternative')
    msg['Subject'] = title
    msg['From'] = '%s <%s>' % ("PaperPlume", EMAIL_FROM)
    msg['To'] = '%s <%s>' % ("client", to_email)

    msg['Reply-to'] = 'xxx'
    msg['Message-id'] = email.utils.make_msgid()
    msg['Date'] = email.utils.formatdate()

    # 构建alternative的text/html部分
    # texthtml = MIMEText('自定义HTML超文本部分', _subtype='html', _charset='UTF-8')
    # msg.attach(texthtml)
    # 读取email.html文件内容
    with open('email.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    html_content = html_content.format(number=number)
    # 构建alternative的text/html部分
    texthtml = MIMEText(html_content, _subtype='html', _charset='UTF-8')
    msg.attach(texthtml)
    # textplain = MIMEText('{}'.format(content), _subtype='plain', _charset='UTF-8')


    try:
        ctxt = ssl.create_default_context()
        ctxt.set_ciphers('DEFAULT')
        client = smtplib.SMTP_SSL('smtpdm.aliyun.com', 465, context=ctxt)
        # client = smtplib.SMTP()
        # client.connect(EMAIL_HOST, EMAIL_PORT)
        # 开启DEBUG模式
        client.set_debuglevel(0)
        client.login(EMAIL_FROM, EMAIL_HOST_PASSWORD)
        client.sendmail(EMAIL_FROM, [to_email], msg.as_string())
        client.quit()
        return True
    except smtplib.SMTPConnectError as e:
        error_msg = '邮件发送失败，连接失败'
    except smtplib.SMTPAuthenticationError as e:
        error_msg = '邮件发送失败，认证错误:'
    except smtplib.SMTPSenderRefused as e:
        error_msg = '邮件发送失败，发件人被拒绝:'
    except smtplib.SMTPRecipientsRefused as e:
        error_msg = '邮件发送失败，收件人被拒绝:'
    except smtplib.SMTPDataError as e:
        error_msg = '邮件发送失败，数据接收拒绝:'
    except smtplib.SMTPException as e:
        error_msg = '邮件发送失败, {}'.format(e.message)
    except Exception as e:
        error_msg = '邮件发送异常, {}'.format(str(e))
    print(error_msg)
    return False


if __name__ == '__main__':
    SendMail("xxx", "🚀 Your Verseeding launch code", "content")

# # files = [r'C:\Users\Downloads\test1.jpg', r'C:\Users\Downloads\test2.jpg']
# # for t in files:
# #     filename = t.rsplit('/', 1)[1]
# #     part_attach1 = MIMEApplication(open(t, 'rb').read())  # 打开附件
# #     part_attach1.add_header('Content-Disposition', 'attachment', filename=filename)  # 为附件命名
# #     msg.attach(part_attach1)  # 添加附件
#
# # #发送url附件
# # files = [r'https://example.oss-cn-shanghai.aliyuncs.com/xxxxxxxxxxx.png']
# # for t in files:
# #     filename=t.rsplit('/', 1)[1]
# #     response = urllib.request.urlopen(t)
# #     part_attach1 = MIMEApplication(response.read())  # 打开附件，非本地文件
# #     part_attach1.add_header('Content-Disposition', 'attachment', filename=filename)  # 为附件命名
# #     msg.attach(part_attach1)  # 添加附件
#
#
# # 发送邮件
# try:
#     # 若需要加密使用SSL，可以这样创建client
#     # client = smtplib.SMTP_SSL('smtpdm.aliyun.com', 465)
#
#     # python 3.10/3.11新版本若出现ssl握手失败,请使用下列方式处理：
#     ctxt = ssl.create_default_context()
#     ctxt.set_ciphers('DEFAULT')
#     client = smtplib.SMTP_SSL('smtpdm.aliyun.com', 465, context=ctxt)
#
#     # SMTP普通端口为25或80
#     client = smtplib.SMTP('smtpdm.aliyun.com', 80)
#     # 开启DEBUG模式
#     client.set_debuglevel(0)
#     # 发件人和认证地址必须一致
#     client.login(username, password)
#     # 备注：若想取到DATA命令返回值,可参考smtplib的sendmail封装方法:
#     # 使用SMTP.mail/SMTP.rcpt/SMTP.data方法
#     # print(receivers)
#     client.sendmail(username, receivers, msg.as_string())  # 支持多个收件人，最多60个
#     client.quit()
#     print('邮件发送成功！')
