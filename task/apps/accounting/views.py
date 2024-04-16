from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from .serializers import CustomUserSerializer
from utils import sendEmail2,crete_random
from .models import CustomUser
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated


class RegisterAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'message':'you are login'},status=status.HTTP_400_BAD_REQUEST)

        user_email=request.data.get('email')
        acount_user=CustomUser.objects.filter(email=user_email)
        if acount_user:
            if acount_user[0].is_active==False:
                acount_user[0].delete()
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            serializer.create(serializer.validated_data)
            active_code = crete_random(5)   


            user=CustomUser.objects.get(email=data['email'])
            user.active_code=active_code
            user.save()
            
            str_active_code=str(active_code)
            email_user=data['email']
            email_subject='Authentication code'
            email_body=f'''<h1 style="color:blue;text-align:center;">Your authentication code  :{str_active_code}</h1>'''
            sendEmail2(email_subject,'',email_body,[email_user])
            
            
            
            request.session['session_user'] = {
                'active_code': str(active_code),
                'email': data['email'],
                'password': '',
                'remember_password': False  
            }
            
            
            return Response(serializer.data,status=status.HTTP_201_CREATED,headers={'Location': '/accounting/verify/'})
            
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#---------------------------------------------------------------------------------------------

class VerifyAPIView(APIView):
    def post(self, request, *args, **kwargs):
        
        session_data = request.session.get('session_user')
        if not session_data:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        if session_data['remember_password']==True:
            session_active_code = session_data['active_code']
            user_active_code = request.data.get('code')
            if user_active_code == session_active_code:
                user=CustomUser.objects.get(email=session_data['email'])
                user.active_code=crete_random(5)
                user.set_password(session_data['password'])
                user.save()
                del request.session['session_user']
                return Response({'message':'Change password successfully'},status=status.HTTP_201_CREATED)
            
                



        session_active_code = session_data['active_code']
        
        user_active_code = request.data.get('code')

        if user_active_code == session_active_code:
            
            user=CustomUser.objects.get(email=session_data['email'])
            user.is_active=True
            user.active_code=crete_random(5)
            user.save()
            
            user_token,w=Token.objects.get_or_create(user=user)
            user_token_string=user_token.key
   
            del request.session['session_user']
            return Response({'message':'Registration was successful','token_is':user_token_string},status=status.HTTP_201_CREATED)
            
        else:
           
            return Response({'error': 'The entered code is invalid'}, status=status.HTTP_400_BAD_REQUEST)

#---------------------------------------------------------------------------------------------
class LoginApiView(APIView):
    def post(self,request,*args,**kwargs):
        username=request.data.get('email')
        password=request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token_is': token.key}, status=status.HTTP_201_CREATED)
            
        else:
            return Response({'error':'The email or password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
            
#---------------------------------------------------------------------------------------------

class LogoutApiView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request,):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logout was successful'}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Logout failed' }, status=status.HTTP_400_BAD_REQUEST)
            
#----------------------------------------------------------------------------------------------
class ChangePasswordView(APIView):
    def post(self,request,*args,**kwargs):
        email=request.data.get('email')
        password=request.data.get('password')
        repassword=request.data.get('repassword')
        try:
            user=CustomUser.objects.get(email=email)
            
        except:
            return Response({'error':'There is no such user'},status=status.HTTP_404_NOT_FOUND)
        
        if password != repassword:
            return Response({'error':'Password and repassword are not the same'},status=status.HTTP_400_BAD_REQUEST)
        
        active_code=crete_random(5)
        user.active_code=active_code
        user.save()
        
        email_user=email
        email_subject='Authentication code'
        email_body=f'''<h1 style="color:blue;text-align:center;">Your authentication code  :{active_code}</h1>'''
        sendEmail2(email_subject,'',email_body,[email_user])
        
        
        request.session['session_user'] = {
                'active_code': str(active_code),
                'email': email,
                'password': password,
                'remember_password': True  
            }
        return Response({'message':'Authentication code sent successfully'},status=status.HTTP_200_OK,headers={'Location': '/accounting/verify/'})