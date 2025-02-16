import email

# 读取邮件文件
with open('222.eml', 'r') as file:
    email_content = file.read()

# 解析邮件
msg = email.message_from_string(email_content)

# 检查是否有多个部分（多个MIME类型）
if msg.is_multipart():
    # 遍历所有部分
    for part in msg.get_payload():
        # 检查部分的MIME类型是否为text/html
        if part.get_content_type() == 'text/html':
            # 提取HTML代码
            html_code = part.get_payload(decode=True).decode('utf-8')
            print(html_code)
else:
    # 检查邮件的MIME类型是否为text/html
    if msg.get_content_type() == 'text/html':
        # 提取HTML代码
        html_code = msg.get_payload(decode=True).decode('utf-8')
        print(html_code)
# 将HTML代码保存到文件
with open('email.html', 'w', encoding='utf-8') as file:
    file.write(html_code)