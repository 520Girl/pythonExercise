# 自动发送邮件 ppwpsbefkgbwbdhc

import smtplib
from getpass import getpass
from email.message import EmailMessage

# EMAIL_ADDRESS = getpass("Email：")
# EMAIL_PASSWORD = getpass("Password：")
EMAIL_ADDRESS = "815842080@qq.com"
EMAIL_PASSWORD = "ppwpsbefkgbwbdhc"

# 链接到smtp 服务器,通过加密的方式
# smtp = smtplib.SMTP("smtp.163.com", 25)
smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
# 登录邮箱
print(smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD))

#发送邮件
sender = EMAIL_ADDRESS
receiver = EMAIL_ADDRESS
subject = "python email subject"
body = "hello , this is an email"
msg = f"Subject: {subject}\n\n{body}"
smtp.sendmail(sender, receiver, msg)
smtp.quit()


