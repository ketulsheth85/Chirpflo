from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.urls import re_path
from rest_framework import routers  


from rest_framework.routers import DefaultRouter

# View and other imports
from Signup.views import *
from Company.views import *
from adminapp.views import *
from django.conf.urls.static import static

from django.shortcuts import redirect

def redirect_to_chirpflo(request):
    return redirect(settings.WEB_URL+'/login')

app_name = 'Signup','Company',

router = DefaultRouter()
router.register('v1/user', UserApi, basename="user")
#Verify OTP
router.register('v1/userprofile', UserProfileAPI, basename="userprofile")
#Login ,Logout
router.register('v1/login', LoginAPI, basename="login")
router.register('v1/logout', LogoutAPI, basename="logout")
#Resend OTP
router.register('v1/resendotp',ResendOTPAPI,basename="resendotp")
#Password Change
router.register('v1/change_password',ChangeUserPasswordAPI,basename="change_password")
#Company API 
router.register('v1/company',CompanyApi,basename="company")
router.register('v1/company_base',CopmanyApi_Base,basename="company_base")

#Admin Panel Url
router.register('v1/get_users_admin',AdminAPI,basename="get_users_admin")
router.register('v1/get_user_chatlog_admin',AdminChatlogAPI,basename="get_user_chatlog_admin")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',redirect_to_chirpflo),
    path('v1/DashboardAPI',DashboardAPI.as_view(),name='DashboardAPI'),
    path('v1/forgetpassword_mail',ForgetPasswordSendMail.as_view(),name='forgetpassword_mail'),
    path('v1/forgetpassword',ForgetPassword.as_view(),name='forgetpassword'),
    path('v1/ChatGPTAPI_',ChatGPTAPI_.as_view(),name='ChatGPTAPI_'),
    path('v1/LoginChatGPTAPI',LoginChatGPTAPI.as_view(),name='LoginChatGPTAPI'),
    path('webhook',webhook.as_view(),name='webhook'),
    path('v1/facebook_authflow_logout',facebook_authflow_logout.as_view(),name='facebook_authflow_logout'),
    path('v1/admin_DashboardAPI',AdminDashboardAPI.as_view(),name='admin_DashboardAPI'),
    path('v1/admin_mailconfig',AdminMailConfig.as_view(),name='admin_mailconfig'),
    path('v1/Knowledge_baseURLAPI',Knowledge_baseURLAPI.as_view(),name='Knowledge_baseURLAPI'),
    path('v1/KB_questionsURLAPI',KB_questionsURLAPI.as_view(),name='KB_questionsURLAPI'),
    path('v1/KB_questionsURLAPI/<pk>',KB_questionsURLAPI.as_view(),name='KB_questionsURLAPI'),
    path('v1/Chat_logAPI/',Chat_logAPI.as_view(),name='Chat_logAPI'),
    path('v1/Chat_logAPI/<int:pk>',Chat_logAPI.as_view(),name='Chat_logAPI'),
    path('v1/Questions_API/',Ques_API.as_view(),name='Ques_API'),
    path('v1/Questions_API/<int:pk>',Ques_API.as_view(),name='Ques_API'),
    path('v1/Questions_ALL_API/',Ques_ALL_API.as_view(),name='Ques_ALL_API'),
    path('v1/Content_DeleteAPI/',Content_DeleteAPI.as_view(),name='Content_DeleteAPI'),
    path('v1/wellcomeSmsApi/',wellcomeSmsApi.as_view(),name='wellcomeSmsApi'),
    path('v1/welcomesms_linkAPI/',welcomesms_linkAPI.as_view(),name='welcomesms_linkAPI'),
    path('v1/Webchat_widgetAPI/',WidgetAPI.as_view(),name='Webchat_widgetAPI'),
    path('v1/Avtar_Image_WidgetAPI/',Avtar_Image_WidgetAPI.as_view(),name='Avtar_Image_WidgetAPI'),
    path('v1/Icons_Image_WidgetAPI/',Icons_Image_WidgetAPI.as_view(),name='Icons_Image_WidgetAPI'),    
    path('v1/Copy_WidgetAPI/',Copy_WidgetAPI.as_view(),name='Copy_WidgetAPI'),
    path('v1/WidgetGetAPI/<pk>',WidgetGetAPI.as_view(),name='WidgetGetAPI'),
    path('v1/Widget_bg_ColorAPI/',Widget_bg_ColorAPI.as_view(),name='Widget_bg_ColorAPI'),
    path('v1/Text_questionsURLAPI',Text_questionsURLAPI.as_view(),name='Text_questionsURLAPI'),
    path('v1/PDF_questionsURLAPI',PDF_questionsURLAPI.as_view(),name='PDF_questionsURLAPI'),
    path('v1/LeadsAPI',LeadsAPI.as_view(),name='LeadsAPI'),
    path('v1/Lead_Infos_API',Lead_Infos_API.as_view(),name='Lead_Infos_API'),
    path('v1/Lead_Infos_API/<pk>',Lead_Infos_API.as_view(),name='Lead_Infos_API'),
    path('v1/Lead_ListAPI',Lead_ListAPI.as_view(),name='Lead_ListAPI'),
    path('v1/Lead_ListAPI/<pk>',Lead_ListAPI.as_view(),name='Lead_ListAPI'),
    path('v1/lead_SortingAPI',lead_SortingAPI.as_view(),name='lead_SortingAPI'),
    path('v1/Create_LeadInformationAPI',Create_LeadInformationAPI.as_view(),name='Create_LeadInformationAPI'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns+=router.urls