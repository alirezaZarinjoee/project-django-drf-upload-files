from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import random
from uuid import uuid4
import os

def sendEmail2(subject,message,html_content,to):#متد ارسال ایمیل
    email_from=settings.EMAIL_HOST_USER
    message1=EmailMultiAlternatives(subject,message,email_from,to)
    message1.attach_alternative(html_content,'text/html')
    message1.send()
    
    
def crete_random(count): #تابع تولید رندوم کدفعال سازی
    import random
    count-=1
    return random.randint(10**count,10**(count+1)-1)


class FileUpload:
    def __init__(self,dir,perfix):
        self.dir=dir
        self.perfix=perfix
    
    def upload_to(self,instance,filename):
        name,ext=os.path.splitext(filename)
        return f'{self.dir}/{self.perfix}/{uuid4()}{ext}'