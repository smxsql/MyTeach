# encoding=utf-8
from random import Random

from users.models import EmailVerifyRecoed
from MyCourse.settings import EMAIL_FROM
# 导入Django自带的用邮箱发送函数
from django.core.mail import send_mail

# 新建一个函数利用随机数生成我们的code
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

# 把code和连接存到数据库中但时候进行检测
def send_register_email(email,send_type="register"):
    email_record = EmailVerifyRecoed()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 利用Django的内部函数send_email去发送email
    # email的标题
    email_title = ""
    # email的正文
    email_body = ""

    if send_type == "register":
        email_title = "天天向上在线网激活连接"
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])

        if send_status:
            pass
    elif send_type == "forget":
        email_title = "天天向上在线网重置密码连接"
        email_body = "请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])

        if send_status:
            pass

def generate_random_str():
    pass


