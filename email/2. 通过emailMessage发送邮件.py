from fileinput import filename
import smtplib
import ssl
from getpass import getpass
from email.message import EmailMessage

EMAIL_ADDRESS = "815842080@qq.com"
EMAIL_PASSWORD = "ppwpsbefkgbwbdhc"

# 链接到smtp 服务器,通过加密的方式
context = ssl.create_default_context()

#发送邮件
sender = EMAIL_ADDRESS
receiver = EMAIL_ADDRESS
subject = "python email subject"
body = "hello , this is an email"
msg = EmailMessage()
msg['subject'] = subject
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS
msg.set_content(body)

# 发送html 文件 和附件
filePath = r"H:\slideVerify\1d.png"
with open(filePath, 'rb') as f:
    filedata = f.read()
msg.add_attachment(filedata, maintype='image', subtype='png', filename=filePath)
# 添加html内容 加入 \运行输入字符串换行 msg.iter_parts() 使用这个方法才能 混合资源一起发送 https://www.cnpython.com/qa/906392
text_part, attachment_part = msg.iter_parts()
text_part.add_alternative('<h1 style="color: red;">python</h1>', subtype='html')

# 查看发送的内容格式
# text_part, attachment_part = msg.iter_parts()
# print(text_part)
# print(attachment_part)

with smtplib.SMTP_SSL("smtp.qq.com", 465,context= context) as smtp: # 执行完成自动关闭
    smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    smtp.send_message( msg)



#! 如果是多人发送的话将 msg['To']改为 list ，再在with 中使用for循环进行遍历发送不同消息
