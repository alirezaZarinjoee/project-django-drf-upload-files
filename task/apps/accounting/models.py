from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone




class CustomUserManager(BaseUserManager):
    
    def creat_user(self,email,name='',family='',active_code=None,gender=None,password=None):
        if not email:
            raise ValueError(' ایمیل باید وارد شود')
        user=self.model(
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,name,family,password=None,active_code=None,gender=None):
        user=self.creat_user(
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password
            
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    
    
    
#--------------------------------------------------------------------
    

class CustomUser(AbstractBaseUser,PermissionsMixin):
    
    email=models.EmailField(verbose_name='ایمیل', max_length=254,unique=True)
    name=models.CharField(verbose_name='نام', max_length=50,blank=True)
    family=models.CharField(verbose_name='نام خانوادگی', max_length=50,blank=True)
    GENDER_CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(verbose_name='جنسیت', max_length=50,choices=GENDER_CHOICES,default='True',null=True,blank=True)
    register_date=models.DateTimeField(verbose_name='تاریخ اضافه شدن',default=timezone.now)
    is_active=models.BooleanField(verbose_name='فعال/غیرفعال',default=False)
    active_code=models.CharField(verbose_name='کد فعال سازی',max_length=100,null=True,blank=True)
    is_admin=models.BooleanField(verbose_name='ادمین',default=False)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['name','family']
    
        
    objects=CustomUserManager()
    
    def __str__(self):
        return self.name+' '+self.family
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'