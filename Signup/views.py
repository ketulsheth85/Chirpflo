from django.contrib.auth.models import User

from .utils import *

from .models import User

from django.utils import timezone
from django.contrib.auth import authenticate,login, logout

from django.shortcuts import get_object_or_404

#Password reset lib, encry-decry
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes

# Serializers imports
from .serializers import *

#rest frame lib
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from rest_framework.views import APIView

from datetime import datetime,timedelta
from Company.models import *
from numerize import numerize


# ========================================== User Signup =================================================

#======= Signup 
class UserApi(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data            
            serializer = UserSerializer(data=data,partial=True) 
            # validation for duplicate email
            user_obj = User.objects.filter(email=data.get('email')).exists()
            if user_obj:
                return Response({'status': "400",
                                'message': 'Email already exists. Please choose a different one.'},
                                status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                user = authenticate(email=data.get('email'), password=data.get('password').strip())
                if user:
                    token = {}
                    SlidingToken.for_user(user)
                    RefreshToken.for_user(user)
                    token["refresh"] = str(RefreshToken.for_user(user))
                    token["access"] = str(RefreshToken.for_user(user).access_token)
                    user_data=serializer.data
                    user_data['accesstoken']=token['access']
                    user_data["refreshtoken"]=token['refresh']
                    ctx = {'user': user_data['first_name'],
                        'otp': user_data['email_otp'],
                        'year':datetime.now().year}
                    result = mail_send(user,"Verify Email",ctx)
                    return Response({'status': status.HTTP_201_CREATED,'message': 'User creation successful. Please check your email.',
                            'data': {'user': user_data}}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Error",data:serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
    

#========= Update, DELETE User And OTP Verification 

class UserProfileAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=(IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        try:
            user=request.user
            if user:
                    serializer = UserSerializer(user)
                    return Response({'status':status.HTTP_200_OK,'message': 'User fetched Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'User not found.', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        try:
            intance=self.get_object()
            data=request.data
            if "email" in data:
                if intance.email != data['email']:
                    if User.objects.filter(email=data['email']).exists():
                        return Response({'status': "400",
                                'message': 'User with this email already exists, Please try a new one'},
                                status=status.HTTP_400_BAD_REQUEST)
                        
            serializers=UserSerializer(intance,data=data,partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response({'status': status.HTTP_200_OK,'message': 'User Updated Successfully.','data':serializers.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': serializers.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return viewsets.ModelViewSet.destroy(self, request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user_obj=request.user
            time=timezone.now()
            if user_obj.email_otp_expiry_time==None:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Please Resend the otp.'},status=status.HTTP_400_BAD_REQUEST)
            elif user_obj.email_otp_expiry_time>=time:
                if user_obj.email_otp==data.get('otp'):
                    user_obj.email_otp=None
                    user_obj.email_otp_expiry_time=None
                    user_obj.is_email_verified=True
                    user_obj.save()
                    return Response({'status': status.HTTP_200_OK,'message': 'Email verification successful.'},status=status.HTTP_200_OK)
                else:                
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Invalid OTP. Please try again.'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Your OTP Expired..!'},status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#================================ Login ===================================================

class LoginAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = LoginSerializer(data=data)
        try:
            if serializer.is_valid():
                email = serializer.data['email'].lower().strip()
                if not User.objects.filter(email=email).exists():
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "User doesn't exits."},status=status.HTTP_400_BAD_REQUEST)
                else:
                    password = serializer.data['password'].strip()
                    user = authenticate(email=email, password=password)
                    if user:
                        if data['type']=="super":
                            if not user.is_superuser:
                                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Admin user needed!"},status=status.HTTP_400_BAD_REQUEST)
                        token = {}
                        SlidingToken.for_user(user)
                        RefreshToken.for_user(user)
                        token["refresh"] = str(RefreshToken.for_user(user))
                        token["access"] = str(RefreshToken.for_user(user).access_token)
                        login(request, user)
                        serializer = UserSerializer(user)
                        userdetails = serializer.data
                        userdetails['access'] = token["access"]
                        userdetails['refresh'] = token["refresh"]
                        return Response({'status': status.HTTP_200_OK,'message': 'Login Successfully.','data':userdetails},status=status.HTTP_200_OK)
                    else:
                        return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Invalid Credentials.'},status=status.HTTP_400_BAD_REQUEST)
            else:
                 return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Error',"data":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#========================================== Logout ========================================================================

class LogoutAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            user=request.user
            logout(request)
            return Response({'status': status.HTTP_200_OK,'message': 'User Logout Successflly','data':""},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#=========================================== Resend OTP ==============================================================

class ResendOTPAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            user=request.user   
            user.email_otp = generate_random_otp(6)
            current_time=timezone.now()+timedelta(seconds=60)
            user.email_otp_expiry_time = current_time
            user.save()
            # Send mail with credentials
            ctx = {'user': user.first_name,
                   'otp': user.email_otp,
                   'year':datetime.now().year}
            result = mail_send(user,"Verify Email",ctx)
            return Response({'status': status.HTTP_200_OK,'message': 'OTP resent successfully.','data':ctx},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#============================================== Change Password =========================================================

class ChangeUserPasswordAPI(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        try:
            serializer = ChangeUserPasswordSerializer(data=request.data)
            serializer.context['user'] = request.user
            serializer.is_valid()
            user = serializer.execute()
            logout(request)
            return Response({'status': status.HTTP_200_OK,'message': 'Password changed successfully,Kindly login again.','data':""},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
 
#============================================== Forgot Password Mail============================================================

class ForgetPasswordSendMail(APIView):
    def post(self,request):
        try:
            data = request.data['email']
            if User.objects.filter(email=data).exists():
                user = User.objects.get(email=data)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                url="https://chirpflo.com/resetpassword/{0}/{1}".format(uidb64,token)
                ctx = {
                    'user':  user.first_name,
                    'email' : "Email :  " + user.email.lower(),
                    'url' : url,
                    'data1':'We received a request to reset your password within InstaGPT!',
                    'data2':'If you did not forgot your password you can safely ignore this email.',
                    'data3':'To Reset Password ,',
                    'url_data':'Reset New Password',
                    'year':datetime.now().year
                }
                result=mail_sendforgot(user,"Forgot Password",ctx)
                print(result)
                return Response({'status': status.HTTP_200_OK,'message': 'Please check your email.','data':ctx },status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Invalid Email'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#============================================== Forgot Password Changed============================================================

class ForgetPassword(APIView):
    def post(self,request):
        try:
            data=request.data
            uid=request.data['uid']
            token=request.data['token']
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if user:
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Invalid Token.'},status=status.HTTP_400_BAD_REQUEST)
                else:
                    if data['new_password']==data['confirm_password']:
                        password=data['confirm_password']
                        user.set_password(password)
                        user.save()
                        return Response({'status': status.HTTP_200_OK,'message': 'Password changed successfully!'},status=status.HTTP_200_OK)
                    elif data['new_password']!=data['confirm_password']:
                        return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Those password don't match"},status=status.HTTP_400_BAD_REQUEST)                        
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "User not found."},status=status.HTTP_400_BAD_REQUEST)                        
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#================================ User Dashboard =====================================================

class DashboardAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            data = request.data
            user=request.user
            if not create_company.objects.filter(email=user).exists():
                ctx = {
                            'user': {'count':00,'since_last_month':00},
                            'message_to_bot' : {"count": 00,'since_last_month':00},
                            'message_from_bot': {"count":00,'since_last_month':00},
                            'conversations':{"count":00,"category":["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],"data": [00, 00, 00,00, 00, 00, 00, 00, 00, 00, 00, 00]},
                            'contact': {"count":00,"category":["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],"data":[00,00,00,00,00, 00, 00, 00, 00, 00, 00, 00]},
                }
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':ctx},status=status.HTTP_200_OK)
            
            comp=create_company.objects.get(email=user)
            if user:
                #-------user
                count_user=set(chat_log.objects.filter(company=comp).filter(createdAt__month__gte=timezone.now().month,createdAt__month__lte=timezone.now().month).values_list('sender_id', flat=True).exclude(sender_id__exact=None))
                #last month user
                last_month_user=set(chat_log.objects.filter(createdAt__month__gte=timezone.now().month-1,createdAt__month__lte=timezone.now().month-1).values_list('sender_id', flat=True).exclude(sender_id__exact=None))
                #-------message to bot 
                message_to_bot=chat_log.objects.filter(company=comp)
                print("all month message_to_bot",message_to_bot.count())
                #last month percentage
                current_month_message_to_bot=chat_log.objects.filter(company=comp).filter(createdAt__month__gte=timezone.now().month,createdAt__month__lte=timezone.now().month)
                last_month_message_to_bot=chat_log.objects.filter(company=comp).filter(createdAt__month__gte=timezone.now().month-1,createdAt__month__lte=timezone.now().month-1)
                #message from bot
                message_from_bot=chat_log.objects.filter(company=comp).exclude(text__exact=None)
                current_message_from_bot=chat_log.objects.filter(company=comp).filter(createdAt__month__gte=timezone.now().month,createdAt__month__lte=timezone.now().month).exclude(text__exact=None)
                last_message_from_bot=chat_log.objects.filter(company=comp).filter(createdAt__month__gte=timezone.now().month-1,createdAt__month__lte=timezone.now().month-1).exclude(text__exact=None)
                #conversation
                conversations=chat_log.objects.filter(company=comp).count()+chat_log.objects.filter(company=comp).exclude(text__exact=None).count()
                #contacts
                contact=set(chat_log.objects.filter(company=comp).values_list('sender_id', flat=True).exclude(sender_id__exact=None))                

                #contact and conversation month graph
                conv_list_data=[]
                contact_list_data=[]
                if data["filter"]['start']==None and data["filter"]['end']==None:
                    for cnt in range(1,13):
                        conv=chat_log.objects.filter(company=comp).filter(createdAt__month__gte=cnt,createdAt__month__lte=cnt).count()+chat_log.objects.filter(company=comp).filter(createdAt__month__gte=cnt,createdAt__month__lte=cnt).exclude(text__exact=None).count()
                        cont=len(set(chat_log.objects.filter(company=comp).filter(createdAt__month__gte=cnt,createdAt__month__lte=cnt).values_list('sender_id', flat=True).exclude(sender_id__exact=None)))
                        conv_list_data.append(conv)
                        contact_list_data.append(cont)
                
                if data["filter"]['start']!=None and data["filter"]['end']!=None:
                    st_date=data["filter"]['start']
                    ed_date=data["filter"]['end']
                    st=datetime.strptime(st_date,"%Y-%m-%d")
                    ed=datetime.strptime(ed_date,"%Y-%m-%d")

                    end_date = ed.replace(hour=23, minute=59, second=59)

                    message_to_bot=message_to_bot.filter(createdAt__gte=st_date,createdAt__lte=end_date)
                    message_from_bot=message_from_bot.filter(createdAt__gte=st_date,createdAt__lte=end_date)
                    conversations=message_to_bot.count()+message_from_bot.count()
                    contact=set(chat_log.objects.filter(company=comp).values_list('sender_id', flat=True).exclude(sender_id__exact=None).filter(createdAt__gte=st_date,createdAt__lte=ed_date))             

                    for cnt in range(1,13):
                        conv=chat_log.objects.filter(createdAt__gte=st_date,createdAt__lte=end_date)
                        cont=chat_log.objects.filter(createdAt__gte=st_date,createdAt__lte=end_date)
                        conv=conv.filter(company=comp).filter(createdAt__month__gte=cnt,createdAt__month__lte=cnt).count()+conv.filter(company=comp).filter(createdAt__month__gte=cnt,createdAt__month__lte=cnt).exclude(text__exact=None).count()
                        cont=set(cont.filter(company=comp).filter(createdAt__month__gte=cnt,createdAt__month__lte=cnt).values_list('sender_id', flat=True).exclude(sender_id__exact=None))
                        conv_list_data.append(conv)
                        contact_list_data.append(len(cont))
                   
                if len(last_month_user)>0:
                    last_month_user_pr=((len(count_user)-len(last_month_user))/len(last_month_user))* 100
                else:
                    last_month_user_pr=00
                if last_month_message_to_bot.count()>0:
                    message_to_bot_pr=round(((current_month_message_to_bot.count()-last_month_message_to_bot.count())/last_month_message_to_bot.count())*100,2)
                else:
                    message_to_bot_pr=00
                if last_message_from_bot.count()>0:
                    message_from_bot_pr=round(((current_message_from_bot.count()-last_message_from_bot.count())/last_message_from_bot.count())*100,2)
                else:
                    message_from_bot_pr=00
    
                ctx = {
                    'user': {'count': len(count_user),'since_last_month':round(last_month_user_pr)},
                    'message_to_bot' : {"count": numerize.numerize(message_to_bot.count()),'since_last_month':message_to_bot_pr},
                    'message_from_bot': {"count":numerize.numerize(message_from_bot.count()),'since_last_month':message_from_bot_pr},
                    'conversations':{"count":numerize.numerize(conversations),"category":["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],"data":conv_list_data},
                    'contact': {"count":len(contact),"category":["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],"data":contact_list_data},
                    }
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':ctx},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'User not found!'},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)


#===================================== User all content delete API (Company , WebSite Data, KnowledgeBase FAQ) ==================================================

class Content_DeleteAPI(APIView): 
    permission_classes = (IsAuthenticated,) 
    def delete(self,request):
        try: 
            user=request.user 
            conv=conversation_memory.objects.filter(user=user)
            conv.delete()
            leads_to_delete = lead.objects.filter(bot__email=user)
            leads_to_delete.delete()
            web=create_company.objects.filter(email=user) 
            web.delete()
            lead_in=lead_information.objects.filter(user=user) 
            lead_in.delete()
            web_=website_ques.objects.filter(user=user)
            web_.delete() 
            kno=knowledge_base_ques.objects.filter(user=user)
            kno.delete()
            kno=webchat_widget.objects.filter(user=user)
            kno.delete()
            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':""},status=status.HTTP_200_OK) 
        except Exception as e: 
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)