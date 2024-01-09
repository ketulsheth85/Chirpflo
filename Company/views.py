from bs4 import BeautifulSoup
from django.http import HttpResponse
from .serializers import *
from rest_framework import status, viewsets
from .models import create_company,User
from rest_framework.response import Response
# Create your views here.

from rest_framework.views import APIView
from .CHATGPT import *

from rest_framework import pagination
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .FAQ import *
import uuid
from InstaGpt.task import *
from PyPDF2 import PdfReader
from pprint import pprint
from django.core.files import File
import os

#================================================================== Company API GET,POST,UPDATE =====================================================================

class CompanyApi(viewsets.ModelViewSet):
    queryset = create_company.objects.all()
    serializer_class = CompanySerializer

    def list(self, request, *args, **kwargs):
        try:
            user=request.user
            if user:
                if create_company.objects.filter(email=user).exists():
                    user_obj = create_company.objects.filter(email=user).get()
                    # serializer = CompanySerializerALL(user_obj)
                    serializer = CompanySerializer(user_obj)
                    return Response({'status':status.HTTP_201_CREATED,'message': 'Company fetched Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status':status.HTTP_200_OK,'message': '', 'data': ""}, status=status.HTTP_200_OK)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'User not found.', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            if create_company.objects.filter(email=request.user).exists():
                return Response({'status': status.HTTP_400_BAD_REQUEST,
                                    'message': 'Company already exists.'},status=status.HTTP_400_BAD_REQUEST)
            if request.user.user_type=="1" or request.user.is_superuser:
                data['email']=request.user.id
                user_obj = create_company.objects.filter(company=data.get('company')).exists()
                if user_obj:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,
                                    'message': 'This company already exists, Please try a new one'},status=status.HTTP_400_BAD_REQUEST)
                if "website" in request.data:
                    from django.core.validators import URLValidator
                    from django.core.exceptions import ValidationError
                    validate = URLValidator()
                    try:
                        validate(request.data["website"])
                    except ValidationError as e:
                        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':list(e)[0], 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
                serializer = CompanySerializer(data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status':status.HTTP_201_CREATED,'message': 'Company created successful.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'Error', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'Admin Account Needed..!', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        try:
            if "website" in request.data:
                if request.data['website']!="":
                    validate = URLValidator()
                    try:
                        validate(request.data["website"])
                    except ValidationError as e:
                        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':list(e)[0], 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
            if "booking_link" in request.data:
                if request.data['booking_link']!="":
                    validate = URLValidator()
                    try:
                        validate(request.data["booking_link"])
                    except ValidationError as e:
                        return Response({'status':status.HTTP_400_BAD_REQUEST,'message':list(e)[0], 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
            instance=self.get_object()
            serializer = CompanySerializer(instance=instance,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_200_OK,'message': 'Company update successful.', 'data': serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CopmanyApi_Base(viewsets.ModelViewSet):
    queryset = create_company.objects.all()
    serializer_class = CompanySerializer_Knowledge_Base

    def list(self, request, *args, **kwargs):
        try:
            user=request.user
            if user:
                try:
                    user_obj = create_company.objects.filter(email=user).get()
                except Exception as e:
                    user_obj =""
                if user_obj!="":
                    serializer = CompanySerializer_Knowledge_Base(user_obj)
                    return Response({'status':status.HTTP_201_CREATED,'message': 'Company fetched Successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'status':status.HTTP_201_CREATED,'message': '', 'data': ""}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status':status.HTTP_400_BAD_REQUEST,'message': 'User not found.', 'data': ""}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        viewsets.ModelViewSet.partial_update(self, request, *args, **kwargs)
        instance=self.get_object()
        serializer = CompanySerializer_Knowledge_Base(instance)
        return Response({'status':status.HTTP_200_OK,'message': 'Company updated Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)

# ============================================================================== CHATGPT API's ===========================================================

# ================================================================Welcome Chat API(Company Bot)
class wellcomeSmsApi(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user=request.user
        if create_company.objects.filter(email=user): 
            user_obj = create_company.objects.filter(email=user).get()
            if lead.objects.filter(bot=user_obj).filter(lead_status=True).exists():
                user_lead=lead.objects.get(bot=user_obj)
                chat_log.objects.create(company=user_obj,prmt=user_lead.welcome_lead_message,text=None,prm_token=00,used_token=00,total_token=00)
                result={
                    "welcome_msg":user_lead.welcome_lead_message,
                    "status": True,
                    "lead_choice": [user_lead.positive_lead_choice,user_lead.continue_lead_choice],
                    "generate_lead_choice":user_lead.generate_lead_choice
                }
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':result},status=status.HTTP_200_OK)
            else:
                result={
                    "welcome_msg":user_obj.welcome_msg,
                    "status": False,
                    "lead_choice":None,                    
                }
                chat_log.objects.create(company=user_obj,prmt=user_obj.welcome_msg,text=None,prm_token=00,used_token=00,total_token=00)
                return Response({'status':status.HTTP_200_OK,'message': 'Wellcome sms Successfully', 'data': result}, status=status.HTTP_200_OK)
        else: 
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message': "Not found."}, status=status.HTTP_400_BAD_REQUEST)

# ================================================================Welcome Login Chat API (Company Demo Bot Link/Widget)
class welcomesms_linkAPI(APIView):
    def get(self, request): 
        try: 
            if request.query_params.get('company',"")!="": 
                if create_company.objects.filter(id=request.query_params['company']).exists(): 
                    comp=create_company.objects.get(id=request.query_params['company'])
                    if lead.objects.filter(bot=comp).filter(lead_status=True).exists():
                        user_lead=lead.objects.get(bot=comp)
                        chat_log.objects.create(company=comp,prmt=user_lead.welcome_lead_message,text=None,prm_token=00,used_token=00,total_token=00)
                        result={
                            "welcome_msg":user_lead.welcome_lead_message,
                            "status": True,
                            "lead_choice": [user_lead.positive_lead_choice,user_lead.continue_lead_choice],
                            "generate_lead_choice": user_lead.generate_lead_choice

                        }
                        return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':result},status=status.HTTP_200_OK)
                    else:
                        result={
                            "welcome_msg":comp.welcome_msg,
                            "status": False,
                            "lead_choice": None,
                            "generate_lead_choice": None

                        }
                        chat_log.objects.create(company=comp,prmt=comp.welcome_msg,text=None,prm_token=00,used_token=00,total_token=00)
                        return Response({'status':status.HTTP_200_OK,'message': 'Wellcome sms Successfully', 'data': result}, status=status.HTTP_200_OK) 
                else: 
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message':"Company details not found!"},status=status.HTTP_400_BAD_REQUEST) 
            else: 
                user=User.objects.filter(is_superuser=True).get() 
                comp=create_company.objects.get(email=user)
                if lead.objects.filter(bot=comp).filter(lead_status=True).exists():
                    user_lead=lead.objects.get(bot=comp)
                    result={
                        "welcome_msg":user_lead.welcome_lead_message,
                        "status": True,
                        "lead_choice": [user_lead.positive_lead_choice,user_lead.continue_lead_choice]
                    }
                    chat_log.objects.create(company=comp,prmt=user_lead.welcome_lead_message,text=None,prm_token=00,used_token=00,total_token=00)
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':result},status=status.HTTP_200_OK)
                else:
                    result={
                            "welcome_msg":comp.welcome_msg,
                            "status": False,
                            "lead_choice": None
                        }                
                    chat_log.objects.create(company=comp,prmt=comp.welcome_msg,text=None,prm_token=00,used_token=00,total_token=00)
                    return Response({'status':status.HTTP_200_OK,'message': 'Wellcome sms Successfully', 'data': result}, status=status.HTTP_200_OK)
        except Exception as e: 
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

# ================================================================ Login Chat API
class LoginChatGPTAPI(APIView):
    def post(self,request):
        try:
            data=request.data
            receip_id=data['session_id']
            if str(data['prompt']).strip()=="":
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Message is empty."},status=status.HTTP_400_BAD_REQUEST)

            if request.query_params.get('company',"")!="":
                # print("1")
                if create_company.objects.filter(id=request.query_params['company']).exists():
                    comp=create_company.objects.get(id=request.query_params['company'])

                    seri=PromtData(comp)
                    user=seri['email']
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message':"Company details not found!"},status=status.HTTP_400_BAD_REQUEST)
            else:
                # print("2")
                user=User.objects.filter(is_superuser=True).get()
                comp=create_company.objects.get(email=user)
                seri=PromtData(comp)
            user_seri_data=seri.data
            if User.objects.filter(email=user_seri_data['email']).exists():
                # print("-----pass")
                user=User.objects.get(email=user_seri_data['email'])
                if conversation_memory.objects.filter(user=user,conversation_type="2").count()>6:
                    conv=conversation_memory.objects.filter(user=user,conversation_type="2")
                    conv.delete()
                    # print("Conv Deleted")

            # print(user_seri_data)
            user_data,responce=CHAT_RESPONCE(data,user_seri_data,comp,"2",receip_id)
            if user_data==None and responce==None:
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':""},status=status.HTTP_200_OK)

            conv=conversation_memory(
                user=user,
                conversation_type="2",
                message=data['prompt'],
                responce=responce)
            conv.save()
            chat_responce=[]
            for message in user_data['text']:
                data=user_data
                data['text']=message
                data['recipient_id']=receip_id
                chat_seri=ChatSerializer(data=user_data,partial=True)
                if chat_seri.is_valid():
                    chat_seri.save()
                    chat_responce.append(chat_seri.data)
                    # if lead.objects.filter(bot=comp).exists():
                    #     lead_=lead.objects.get(bot=comp)
                    #     if lead_.lead_status==True and message.lower().strip()==lead_.closing_lead_message.lower().strip():
                    #         chat_responce.append({
                    #             "closing_lead_choice": [lead_.positive_lead_closing_choice,lead_.continue_lead_closing_choice]
                    #         })
                    #     elif lead_.lead_status==True and chat_seri.data['prmt'].lower().strip()==lead_.positive_lead_closing_choice.lower().strip():
                    #         chat_responce.append({
                    #             "closing_chatbot": True
                    #         })

                else:
                    print(chat_seri.errors)
            sum_total=chat_log.objects.filter(company=comp).aggregate(Sum('total_token'))
            comp.company_total_token=sum_total["total_token__sum"]
            comp.save()
            user_chat=conversation_memory.objects.filter(user__email=seri.data['email'],conversation_type="2").order_by("id").values()
            if user_chat.count()>2 and lead_information.objects.filter(user__email=seri.data['email'],recipient_id=receip_id).exists():
                print("lead Store----------------------------------------------------------------------------------------")
                user_chat=conversation_memory.objects.filter(user__email=seri.data['email'],conversation_type="2").order_by("id").values()
                conversation_text = '\n'.join(d['message'] +"\n" + str(d['responce']) for d in user_chat)
                print("conversation-----------------------------\n",conversation_text)
                leads = exract_lead_information(conversation_text)
                print(leads)
                if leads!=None:
                    lead_in=lead_information.objects.get(user__email=seri.data['email'],recipient_id=receip_id)
                    if "name" in leads:
                        lead_in.name=leads['name']
                    if "email" in leads:
                        lead_in.email=leads['email']
                    if "phone" in leads:
                        lead_in.phone_number=leads['phone']
                    if "lead_information" in leads:
                        lead_in.lead_summary=leads['lead_information']   
                    lead_in.save()

            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':chat_responce},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,format=None):
        try: 
            if request.query_params.get('company',"")!="":
                if create_company.objects.filter(id=request.query_params['company']).exists(): 
                    comp=create_company.objects.get(id=request.query_params['company'])
                    user=User.objects.get(id=comp.email.id)
                    # conv=conversation_memory.objects.filter(user=comp.email).filter(conversation_type="2")
                    # conv.delete()
                else: 
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message':"Company details not found!"},status=status.HTTP_400_BAD_REQUEST) 
            else:
                user=User.objects.filter(is_superuser=True).get()
            
            if user:               
                conv=conversation_memory.objects.filter(user=user,conversation_type="2")
                conv.delete() 
                return Response({'status':status.HTTP_200_OK,'message': 'Chat Deleted Successfully!'}, status=status.HTTP_200_OK) 
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message':"User details not found!"},status=status.HTTP_400_BAD_REQUEST) 

        except Exception as e: 
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

# =================================================================  Company Chat API
class ChatGPTAPI_(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            data=request.data  
            receip_id=data['session_id']          
            user=request.user            
            if create_company.objects.filter(email=user).exists():
                comp=create_company.objects.get(email=user)
                if str(data['prompt']).strip()=="":
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Message is empty."},status=status.HTTP_400_BAD_REQUEST)
                seri=PromtData(comp)
                user_data=seri.data
                if conversation_memory.objects.filter(user=user,conversation_type="1").count()>15:
                    conv=conversation_memory.objects.filter(user=user,conversation_type="1")
                    conv.delete()
                    # print("Conv Deleted")
                
                user_data,responce=CHAT_RESPONCE(data,user_data,comp,"1",receip_id)
                if user_data==None and responce==None:
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':""},status=status.HTTP_200_OK)

                conv=conversation_memory(
                    user=user,
                    conversation_type="1",
                    message=data['prompt'],
                    responce=responce)
                conv.save()
                chat_responce=[]
                for message in user_data['text']:
                    data=user_data
                    data['text']=message
                    data['recipient_id']=receip_id
                    chat_seri=ChatSerializer(data=user_data,partial=True)
                    if chat_seri.is_valid():
                        chat_seri.save()
                        chat_responce.append(chat_seri.data)
                    #     if lead.objects.filter(bot=comp).exists():
                    #         lead_=lead.objects.get(bot=comp)
                    #         if lead_.lead_status==True and message.lower().strip()==lead_.closing_lead_message.lower().strip():
                    #             chat_responce.append({
                    #                 "closing_lead_choice": [lead_.positive_lead_closing_choice,lead_.continue_lead_closing_choice]
                    #             })
                    #         elif lead_.lead_status==True and chat_seri.data['prmt'].lower().strip()==lead_.positive_lead_closing_choice.lower().strip():
                    #             chat_responce.append({
                    #                 "closing_chatbot": True
                    #             })
                    else:
                        print(chat_seri.errors)
                sum_total=chat_log.objects.filter(company=comp).aggregate(Sum('total_token'))
                comp.company_total_token=sum_total["total_token__sum"]
                comp.save()
                user_chat=conversation_memory.objects.filter(user__email=seri.data['email'],conversation_type="1").order_by("id").values()
                print(user_chat,"\n_------------------------------------------ COnversation------------------------------")
                if user_chat.count()>1 and lead_information.objects.filter(user__email=seri.data['email'],recipient_id=receip_id).exists():
                    print("lead Store----------------------------------------------------------------------------------------")
                    user_chat=conversation_memory.objects.filter(user__email=seri.data['email'],conversation_type="1").order_by("id").values()
                    conversation_text = '\n'.join(d['message'] +"\n" + str(d['responce']) for d in user_chat)
                    print("conversation text ----------------------------------------\n",conversation_text)
                    leads = exract_lead_information(conversation_text)
                    print(leads)
                    if leads!=None:
                        lead_in=lead_information.objects.get(user__email=seri.data['email'],recipient_id=receip_id)
                        if "name" in leads:
                            lead_in.name=leads['name']
                        if "email" in leads:
                            lead_in.email=leads['email']
                        if "phone" in leads:
                            lead_in.phone_number=leads['phone']
                        if "lead_information" in leads:
                            lead_in.lead_summary=leads['lead_information']
                        lead_in.save()
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':chat_responce},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Please create the company.','data':""},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status':status.HTTP_400_BAD_REQUEST,'message': "Responce not getting from server","data":str(e)},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request): 
        user=request.user 
        if create_company.objects.filter(email=user).exists(): 
            conv=conversation_memory.objects.filter(user=user,conversation_type="1")
            conv.delete() 
            return Response({'status': status.HTTP_200_OK,'message': 'Chat Deleted Successfully!'},status=status.HTTP_200_OK) 
        else: 
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Please create the company.','data':""},status=status.HTTP_400_BAD_REQUEST)

# ====================================================================== Webhook Instagram CHAT API

class webhook(APIView):
    #Verify webhook
    def get(self,request):
        try:
            mode=request.GET.get('hub.mode', None)
            challenge=request.GET.get('hub.challenge', None)
            token=request.GET.get('hub.verify_token', None)
            if mode=="subscribe" and token=="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":
                return HttpResponse(request.GET.get('hub.challenge', None),200)
            else:
                return HttpResponse(request.GET.get('hub.challenge', None),400)
        except Exception as e:
            return HttpResponse({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

    #received msg from insta using webhook
    def post(self,request):
        try:
            data=request.data
            # pprint(data)
            prm_data={}

            print("recip",data['entry'][0]['messaging'][0]['recipient']['id'])
            print("message",data['entry'][0]["messaging"][0]["message"]["text"])
            print("sender",data['entry'][0]["messaging"][0]["sender"]["id"])
            if str(data['entry'][0]["messaging"][0]["message"]["text"]).strip()=="":
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Message Not Found."},status=status.HTTP_400_BAD_REQUEST)
            elif create_company.objects.filter(facebook_page_id=data['entry'][0]['messaging'][0]['recipient']['id']).exists():
                comp=create_company.objects.get(facebook_page_id=data['entry'][0]['messaging'][0]['recipient']['id'])
                if comp.is_autoresponce:
                    count=chat_log.objects.filter(company=comp).count()
                    seri=PromtData(comp)
                    user_data_serilizer=seri.data
                    prm_data['prompt']=str(data['entry'][0]["messaging"][0]["message"]["text"]).strip()
                    if count>=2000:
                        user_data={
                            "company":comp.id,
                            "prmt":prm_data['prompt'],
                            "text":"For further information, Please contact us the email : {0} and call us at {1}".format(comp.email,comp.website),
                            "prm_token":00,
                            "used_token":00,
                            "total_token":00,
                            "recipient_id":None,
                            "sender_id":None
                        }
                    else:
                        user_data=CHAT_RESPONCE(prm_data,user_data_serilizer,comp)
                    chat_responce=[]
                    for message in user_data['text']:
                        data=user_data
                        data['text']=message
                        chat_seri=ChatSerializer(data=user_data,partial=True)
                        if chat_seri.is_valid():
                            chat_seri.save()
                            chat_responce.append(chat_seri.data)
                        else:
                            print(chat_seri.errors)
                    sum_total=chat_log.objects.filter(company=comp).aggregate(Sum('total_token'))
                    comp.company_total_token=sum_total["total_token__sum"]
                    comp.save()
                    if comp.facebook_page_access_token_expire_time>=timezone.now().date():
                        resp=insta_dm(data['entry'][0]["messaging"][0]["sender"]["id"],user_data['text'],comp.facebook_page_access_token)
                        return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':{"chatgpt_responce":user_data,"insta_responce":resp}},status=status.HTTP_200_OK)
                    else:
                        return Response({'status': status.HTTP_400_BAD_REQUEST,'message':"token expire"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Auto respomce is off"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "User not found in system"},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#============================================Social Auth Logout API =====================================================
class facebook_authflow_logout(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        user=request.user
        data=request.data
        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            try:
                if data['logout']==True:
                    user_data=User.objects.get(email=user)
                    user_data.is_insta=False
                    user_data.is_facebook=False
                    user_data.save()                    
                    comp.facebook_user_access_token=None
                    comp.facebook_page_id=None
                    comp.facebook_page_access_token=None
                    comp.facebook_page_access_token_expire_time=None
                    comp.save()
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':""},status=status.HTTP_200_OK)                    
            except Exception as e:                   
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Logout failed,Please try again!",'data':str(e)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)
        
#=================================================== Web Scapper ============================================================================
#============================= Get Urls from website
class Knowledge_baseURLAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            data= request.data            
            user=request.user
            url = data['url']
            # response = requests.get(url)
            USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
            headers = {"user-agent": USER_AGENT}
            response = requests.get(url, headers=headers)
            sleep(2)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content,features="html.parser")
                urls = set()
                scan=[]
                if soup.find_all('a')==[]:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "No results found. Please check the URL and try again. Contact us for support if needed."},status=status.HTTP_400_BAD_REQUEST)
                
                for link in soup.find_all('a'):
                    page_url=str(link.get('href'))
                    # print(page_url)
                
                    if url in page_url:
                        urls.add(page_url)
                    else:
                        if url[-1]=="/":
                            # urls.add(url+page_url[1:])
                            if page_url.startswith("/"):
                                urls.add(url+page_url[1:])
                        
                            elif not page_url.startswith("/"):
                                if page_url==None:
                                    pass                    
                                elif page_url.startswith("http"):
                                    pass
                                elif page_url.startswith("https"):
                                    pass
                                else:
                                    urls.add(url+page_url)
                        else:
                            if page_url.startswith("/"):
                                urls.add(url+page_url)
                                if website_ques.objects.filter(user=user).filter(website_url=url+page_url).exists():
                                    scan.append(True)
                                else:
                                    scan.append(False)

                            elif not page_url.startswith("/"):
                                if page_url==None:
                                    pass 
                                elif ":" or "+" in page_url:
                                    pass
                                elif page_url.startswith("http"):
                                    pass
                                elif page_url.startswith("https"):
                                    pass
                                else:
                                    urls.add(url+"/"+page_url)
                user_web_data=[]
                for url in urls:
                    url_={}
                    url_['url']=url
                    if website_ques.objects.filter(user=user).filter(website_url=url).exists():
                        url_['scan']=True
                    else:
                        url_['scan']=False
                    user_web_data.append(url_)

                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':user_web_data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "No results found. Please check the URL and try again. Contact us for support if needed."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

# ====================== Generate FAQ by URL'S
class KB_questionsURLAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,pk):
        pk=pk
        from celery.result import AsyncResult
        result = AsyncResult(pk)
        # print(result.state)  # will be set to PROGRESS_STATE
        # print(result)
        if knowledge_base_ques.objects.filter(user__id=request.user.id).exclude(source="3").count()>=150:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "The FAQ has reached 150 questions limit!"},status=status.HTTP_400_BAD_REQUEST)

        process = MyLongProcess.objects.get(active_uuid=pk)
        data={
            "percentange":process.percentage_sending,
            "success_url":process.success,
            "total_url":process.total
        }
        return Response({'status': status.HTTP_200_OK,'message': f'Extracting Knowledge base FAQ in Background.','data':data},status=status.HTTP_200_OK)

    def post(self,request):
        data= request.data
        urls = data['url_links']
        user=request.user
        if user:
            process = MyLongProcess.objects.create(user=user,active_uuid=uuid.uuid4(), name="task", total=len(urls))
            faq_questions_task.delay(user.email,urls,process.active_uuid)
            return Response({'status': status.HTTP_200_OK,'message': f'Extracting Knowledge base FAQ in Background.','task_id':process.active_uuid},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Users profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)

# ====================== Generate FAQ by TEXT and STORE as INFORMATIO FOR BOT RESPONCE
class Text_questionsURLAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user=request.user
        if user:
            user=User.objects.get(email=user)
            comp=create_company.objects.get(email=user)
            seri=PromtData(comp)
        return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data['text_information']},status=status.HTTP_200_OK)

    def patch(self,request):
        user=request.user
        data= request.data
        if user:
            txt = data['text']
            # if txt=="":
            #     return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Empty text field."},status=status.HTTP_400_BAD_REQUEST)
            user=User.objects.get(email=user)
            comp=create_company.objects.get(email=user)
            comp.text_information=txt
            comp.save()
            return Response({'status': status.HTTP_200_OK,'message': f'Text added successful.'},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Users profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)

# ====================== Generate FAQ by PDF(Documents)
class PDF_questionsURLAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        user=request.user
        if user:
            user=User.objects.get(email=user)
            comp=create_company.objects.get(email=user)
            seri=Document_serilizer(comp)
            # doc=seri.data['pdf_doc']
            # print(doc.LastModified)
            if seri.data['pdf_information']!=None:
                word_count=len(str(seri.data['pdf_information']).split())
                upload_at=comp.pdf_doc.file.obj.last_modified

            else:
                word_count=0
                upload_at=None
            response_data={
                "pdf_url":seri.data['pdf_doc'],
                "name":comp.pdf_doc.name,
                "word_count":word_count,
                "upload_at":upload_at
            }
            print(seri.data)        
        return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':response_data},status=status.HTTP_200_OK)

    def patch(self,request):
        user=request.user
        if user:
            pdf_data= request.FILES['pdf']
            name = pdf_data.name
            extension = name.split(".")[-1]
            available_extensions = ['pdf']
            text=""
            if extension.lower() not in available_extensions:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Unsupported file format. Please use {} files".format(available_extensions[0])},status=status.HTTP_400_BAD_REQUEST)            
            try:
                reader = PdfReader(pdf_data)
            except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Can not read the file!."},status=status.HTTP_400_BAD_REQUEST)

            for i in range(len(reader.pages)):
                text += reader.pages[i].extract_text()
            # print(text)
            user=User.objects.get(email=user)
            comp=create_company.objects.get(email=user)
            data={}
            if comp.pdf_doc:
                comp.pdf_doc.delete(save=False)
            data['pdf_doc']=pdf_data
            data['pdf_information']=text
            # print(text)
            seri=Document_serilizer(comp,data=data,partial=True)
            if seri.is_valid():
                seri.save()
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message':"Can't read the text,please change the file coding format to utf-8.","data": seri.errors},status=status.HTTP_400_BAD_REQUEST)            

            return Response({'status': status.HTTP_200_OK,'message': f'PDF upload successful.',"data":seri.data['pdf_doc']},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Users profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        user=request.user
        if user:
            user=User.objects.get(email=user)
            comp=create_company.objects.get(email=user)
            if comp.pdf_doc:
                comp.pdf_doc.delete(save=False)
                comp.pdf_doc=None
                comp.pdf_information=None
                comp.save()
            return Response({'status': status.HTTP_200_OK,'message': f'PDF deleted successful.'},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Users profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)

#================================================================== Questions API's ===========================================================================
class Ques_API(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user=request.user
        data=request.data
        try:
            ques=knowledge_base_ques.objects.filter(user=user).filter(source=data['source']).order_by("id")
            serializer = Ques_Serializer(ques,many=True)
            web=website_ques.objects.filter(user=user)
            web_serializer = Web_Ques_Serializer(web,many=True)
            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializer.data,"web":web_serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request,pk):
        if knowledge_base_ques.objects.filter(id=pk).exists():
            ques = knowledge_base_ques.objects.get(id=pk)
            # print(request.data)
            data=request.data
            data['source_name']=""
            # print(ques)
            try:
                serializer = Ques_Serializer(ques, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    user_data=serializer.data
                    return Response({'status': status.HTTP_200_OK,'message': 'Message successfully updated.','data':user_data},status=status.HTTP_200_OK)
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': 'Error!','data':""},status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Question not found"},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):        
        if knowledge_base_ques.objects.filter(id=pk).exists():
            try:
                user=request.user
                ques = knowledge_base_ques.objects.get(id=pk)
                if ques.source_name!="":
                    if not knowledge_base_ques.objects.filter(user=user).filter(source_name=ques.source_name).count()>1:                    
                        ques = knowledge_base_ques.objects.get(id=pk)
                        web=website_ques.objects.filter(user=user).filter(website_url=ques.source_name)
                        web.delete()
                ques.delete()
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':""},status=status.HTTP_200_OK)
            except Exception as e:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Not found!"},status=status.HTTP_400_BAD_REQUEST)
       
class Ques_ALL_API(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        user=request.user
        data=request.data
        data['questions']=data['questions'].strip()
        data['answers']=data['answers'].strip()
        if data['questions']=="" and data['answers']=="":
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Enter The Questions and Answers!"},status=status.HTTP_400_BAD_REQUEST)
        elif data['questions']=="":
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Enter The Questions!"},status=status.HTTP_400_BAD_REQUEST)
        elif data['answers']=="":
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Enter The Answers!"},status=status.HTTP_400_BAD_REQUEST)
        elif knowledge_base_ques.objects.filter(user=user).exclude(source="3").count()>=150:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "The FAQ has reached 150 questions limit!"},status=status.HTTP_400_BAD_REQUEST)

        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            company=str(comp.company)
        else:
            company=""
        serializer = Ques_Serializer(data={"user":user.id,"source":"1","source_name":"","questions":data['questions'],"answers":data['answers']})
        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_200_OK,'message': 'Question and answer created successful.','data':serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):   
        data=request.data
        user=request.user
        try:
            if data["source"]!="1" and data["source"]!="3":
                if website_ques.objects.filter(user=user).exists():                    
                    web=website_ques.objects.filter(user=user)
                    for w in web:
                        w.delete()
                    # print("get")
                if knowledge_base_ques.objects.filter(user=user).filter(source="2").exists():
                    ques = knowledge_base_ques.objects.filter(user=user).filter(source="2")
                    for q in ques:
                        q.delete()
            elif data["source"]=="3":
                if knowledge_base_ques.objects.filter(user=user).filter(source="3").exists():
                    ques = knowledge_base_ques.objects.filter(user=user).filter(source="3")
                    for q in ques:
                        q.delete()              
            else:
                if knowledge_base_ques.objects.filter(user=user).filter(source="1").exists():
                    ques = knowledge_base_ques.objects.filter(user=user).filter(source="1")
                    for q in ques:
                        q.delete()            
            return Response({'status': status.HTTP_200_OK,'message': 'All FAQs cleared successfully.','data':""},status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)


#================================================ Chatlog ==========================================================================

#========================== Edit the Text Sms ==========================================
class Chat_logAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user=request.user
        try:
            if create_company.objects.filter(email=user).exists():
                comp=create_company.objects.get(email=user)
                chat = chat_log.objects.filter(company=comp).filter(sender_id=None).order_by('-id')
                serializer = Chatlog_Serializer(chat,many=True)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Company profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request,pk):
        user=request.user
        chat = chat_log.objects.get(id=pk)
        try:
            if request.data['text']=="":
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Empty text field."},status=status.HTTP_400_BAD_REQUEST)

            cht_serializer = Chatlog_Serializer(chat, data=request.data, partial=True)
            # print("-------------------------------")
            if cht_serializer.is_valid():
                cht_serializer.save()
                chat_data=cht_serializer.data
                # print("-------------",chat_data)
                # print(knowledge_base_ques.objects.filter(user=user).filter(source="3").filter(questions=chat_data['prmt']).exists())
                if knowledge_base_ques.objects.filter(user=user).filter(source="3").filter(questions=chat_data['prmt']).exists():
                # if knowledge_base_ques.objects.filter(user=user).filter(questions__icontains=chat_data['prmt']).order_by("-id").exists():
                    knw=knowledge_base_ques.objects.filter(user=user).filter(source="3").filter(questions=chat_data['prmt']).order_by("-id")[0]
                    knw_data={
                        "source":"3",
                        "source_name": "",
                        "questions":chat_data['prmt'],
                        "answers":chat_data['text'],
                    }
                    serializer = Ques_Serializer(knw,data=knw_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                else:
                    knw_data={
                        "user":user.id,
                        "source":"3",
                        "source_name": "",
                        "questions":chat_data['prmt'],
                        "answers":chat_data['text'],
                    }
                    # print(knw_data)
                    serializer = Ques_Serializer(data=knw_data)
                    if serializer.is_valid():
                        serializer.save()
                        # print(serializer.data)
                    else:
                        print(serializer.errors)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':""},status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

#========================================== Chat Widget API's =====================================================
class WidgetAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            if webchat_widget.objects.filter(user=user).exists():
                web_wid=webchat_widget.objects.get(user=user)
                seri=WebWidgetSerializer(web_wid)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK)
            else:                
                web_wid=webchat_widget.objects.create(user=user)
                seri=WebWidgetSerializer(web_wid)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            wid=webchat_widget.objects.get(user=user)
            # print("default_launcher_icon----------------------",str(request.data['default_launcher_icon']))
            data={}
            data['name']=request.data['name']
            data['popup_status']=request.data['popup_status']
            data['timer_count']=request.data['timer_count']
            data['heading']=request.data['heading']
            data['sub_heading']=request.data['sub_heading']
            data['status']=request.data['status']
            data['color']=request.data['color']
            data['background_color']=request.data['background_color']
               
            data['client_bubble_color']=request.data['client_bubble_color']
            data['text_color']=request.data['text_color']
            data['bubble_text_color']=request.data['bubble_text_color']
            data['website']=request.data['website']
            
            if str(request.data['default_launcher_icon'])=="":
                if wid.launcher_icon:
                    data['launcher_icon_status']=True
                else:
                    data['default_launcher_icon']=wid.default_launcher_icon

            elif str(request.data['default_launcher_icon'])!=wid.default_launcher_icon:
                data['default_launcher_icon']=str(request.data['default_launcher_icon'])
                wid.launcher_icon_status= False
                wid.launcher_icon.delete(save=False)
                data['launcher_icon']=None

            for key, value in data.items():
                if value == 'null':
                    data[key] = None
            seri=WebWidgetEditSerializer(wid,data=data,partial=True)
            if seri.is_valid():
                seri.save()
                seri=WebWidgetSerializer(wid)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error!","data":seri.errors},status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        user=request.user
        wid=webchat_widget.objects.get(user=user)
        # Boto s3 delete file upload
        wid.chatbot_avtar.delete(save=False) 
        wid.launcher_icon.delete(save=False)
        wid.delete()
        return Response({'status': status.HTTP_200_OK,'message': "Sucess",'data':""},status=status.HTTP_200_OK)

class Avtar_Image_WidgetAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def patch(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            wid=webchat_widget.objects.get(user=user)
            data={}
            chatbot_avtar = request.FILES['chatbot_avtar']
            file_name = chatbot_avtar.name
            extension = file_name.split(".")[-1]
            available_extensions = ('jpg', 'png', 'jpeg', 'webp')
            if extension.lower() not in available_extensions:      
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Unsupported file format. Please use - {} files".format(available_extensions),'data':""},status=status.HTTP_400_BAD_REQUEST)

            if chatbot_avtar!=wid.chatbot_avtar:
                if wid.chatbot_avtar!="default_avtar_icon_chatgpt_bucket_media.svg":
                    wid.chatbot_avtar.delete(save=False) 
                    data['chatbot_avtar']=chatbot_avtar
                else:
                    data['chatbot_avtar']=chatbot_avtar
            seri=Avtar_Image_WidgetSerializer(wid,data=data,partial=True)
            if seri.is_valid():
                seri.save()
                return Response({'status': status.HTTP_200_OK,'message': 'Avatar update successful!','data':seri.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error",'data':seri.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

class Icons_Image_WidgetAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def patch(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            wid=webchat_widget.objects.get(user=user)
            data={}
            launcher_icon = request.FILES['launcher_icon']
            file_name = launcher_icon.name
            extension = file_name.split(".")[-1]
            available_extensions = ('jpg', 'png', 'jpeg', 'webp')
            if extension.lower() not in available_extensions:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Unsupported file format. Please use - {} files".format(available_extensions),'data':""},status=status.HTTP_400_BAD_REQUEST)

            if launcher_icon!=wid.launcher_icon:
                wid.default_launcher_icon=None
                wid.save()
                wid.launcher_icon.delete(save=False)
                data['launcher_icon_status']=True
                data['launcher_icon']=launcher_icon
            data['launcher_icon']=launcher_icon
            seri=Icon_Image_WidgetSerializer(wid,data=data,partial=True)
            if seri.is_valid():
                seri.save()
                return Response({'status': status.HTTP_200_OK,'message': 'Launcher icon update successful!','data':seri.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error",'data':seri.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

class Widget_bg_ColorAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def patch(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            wid=webchat_widget.objects.get(user=user)
            data={}
            bg_chatbot = request.FILES['bg_chatbot']
            file_name = bg_chatbot.name
            extension = file_name.split(".")[-1]
            available_extensions = ('jpg', 'png', 'jpeg', 'webp')
            if extension.lower() not in available_extensions:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Unsupported file format. Please use - {} files".format(available_extensions),'data':""},status=status.HTTP_400_BAD_REQUEST)

            if bg_chatbot!=wid.bg_chatbot:
                wid.bg_chatbot.delete(save=False)
                data['bg_chatbot']=bg_chatbot
            seri=ChatBot_bgimage_WidgetSerializer(wid,data=data,partial=True)
            if seri.is_valid():
                seri.save()
                return Response({'status': status.HTTP_200_OK,'message': 'Background image update successful.','data':seri.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error",'data':seri.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request):
        user=request.user
        wid=webchat_widget.objects.get(user=user)
        # Boto s3 delete file upload
        wid.bg_chatbot.delete(save=False)
        wid.bg_chatbot=None
        wid.save()
        return Response({'status': status.HTTP_200_OK,'message': "Background image deleted successful.",'data':""},status=status.HTTP_200_OK)

class Copy_WidgetAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            if webchat_widget.objects.filter(user=user).exists():
                web_wid=webchat_widget.objects.get(user=user)
                seri=Widget_Js_ScriptSerializer(web_wid)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK)
            else:                
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the widget."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            wid=webchat_widget.objects.get(user=user)
            name=f"{wid.id}_js"
            js=request.data['js']
            data={}
            with open(f"{name}.js", 'w') as fp:
                fp.write(js)
            fp.close()
            js_script_file = File(open(f'{name}.js','rb'))
            if wid.js_script_file!=None:
                wid.js_script_file.delete(save=False)
            data['js_script_file']=js_script_file
            seri=Widget_Js_ScriptSerializer(wid,data=data,partial=True)
            if seri.is_valid():
                seri.save()
                os.remove(f'{name}.js')
                return Response({'status': status.HTTP_200_OK,'message': 'Icon Successfully Updated!','data':seri.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error",'data':seri.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

class WidgetGetAPI(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self,request,pk):
        user=request.user
        if webchat_widget.objects.filter(id=pk).exists():
            web_wid=webchat_widget.objects.get(id=pk)
            seri=WidgetGetSerializer(web_wid)
            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK)
        else:                
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the widget."},status=status.HTTP_400_BAD_REQUEST)

#============================================= Live Insta chat ===========================================================
# class InstaMSG(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self,request):
#         user=request.user
#         if create_company.objects.filter(email=user).exists():
#             comp=create_company.objects.get(email=user)
#             if comp.facebook_page_access_token_expire_time==None:
#                 return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please login again,Session expired."},status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 message=[]
#                 fields="name,participants"
#                 get_insta_user_message=get_all_user_insta_dm(fields,comp.facebook_page_access_token)
#                 for i in get_insta_user_message['data']:
#                     user_prfile=get_user_insta_profile_dm(i['participants']['data'][1]['id'],comp.facebook_page_access_token)
#                     # i['participants']['data'][1]['data']=user_prfile
#                     i['profile_pic']=user_prfile['profile_pic']
#             return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':get_insta_user_message['data']},status=status.HTTP_200_OK)
#         else:
#             return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)
    
#     def post(self,request):
#         user=request.user
#         data=request.data
#         if create_company.objects.filter(email=user).exists():
#             comp=create_company.objects.get(email=user)

#             if comp.facebook_page_access_token_expire_time==None:
#                 return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please login again,Session expired."},status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 message=[]
#                 get_insta_user_message=get_insta_messages(data["id"],comp.facebook_page_access_token)
#                 # for i in get_insta_user_message['data']:
#                 #     user_prfile=get_user_insta_profile_dm(i['participants']['data'][1]['id'],comp.facebook_page_access_token)
#                 #     i['profile_pic']=user_prfile['profile_pic']
#             return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':get_insta_user_message},status=status.HTTP_200_OK)
#         else:
#             return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

# class InstaMSG(APIView):
#     permission_classes = (IsAuthenticated,)
#     def post(self,request):
#         user=request.user
#         data=request.data
#         kwn=knowledge_base_ques.objects
#         # # memory.chat_memory.add_user_message(data['prompt'])
#         # template="""
#         # PERSONALITY: you are a Marketing specialist of IPL company known as AA.You are only Marketing specialist.You are a Marketing specialist for IPL.Your job is to assist customers with any questions they have about the products or services offered by the company based on the information in the knowledge hub. with your answers it should be clear, concise, and specific. It should also be engaging and relevant to the task or conversation at hand. You are encouraged to engage with customers in a friendly and helpful manner, and to make a personal connection by asking for their name and remembering it throughout the conversation. Your goal is to provide outstanding customer service and ensure that each customer leaves the conversation feeling satisfied with their experience.
#         # INFORMATION TO GATHER:[ Customer Email, Customer Name]
#         # CALL TO ACTION: Information will be send to the Link soon.
#         # you are smart-question answering skills.
#         # Current date:2023-04-20 06:06:02.554818.
#         # Make this in the voice of AA.
#         # {history}
#         # Human: {human_input}
#         # Assistant:"""

#         # prompt = PromptTemplate(
#         #     input_variables=["history","human_input"], 
#         #     template=template
#         # )
#         # chatgpt_chain = LLMChain(    
#         #     llm=OpenAI(temperature=0,openai_api_key="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",model_name='gpt-3.5-turbo'),
#         #     prompt=prompt, 
#         #     verbose=True, 
#         #     memory=memory,
#         # )
#         # with get_openai_callback() as cb:
#         #     output = chatgpt_chain.predict(human_input=data['prompt'])
#         #     print(cb)
#         # memory.save_context({"input": data['prompt']}, {"ouput": output})        
#         # return Response({'status':status.HTTP_200_OK,'message': 'Wellcome sms Successfully', 'data': output}, status=status.HTTP_200_OK)

#         if create_company.objects.filter(email=user).exists():
#             comp=create_company.objects.get(email=user)
#             seri=PromtData(comp)
#             user_data=seri.data
#             mesg=boot(data,user_data,comp)
#             return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':mesg},status=status.HTTP_200_OK)
#         else:
#             return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

# ================================================================== Bot Lead Generation ======================================================================
class LeadsAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            if lead.objects.filter(bot=comp).exists():
                web_wid=lead.objects.get(bot=comp)
                seri=lead_view_serilizer(web_wid)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':seri.data},status=status.HTTP_200_OK)
            else:                
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the lead."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        user=request.user

        data=request.data
        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            data['bot']=comp.id
            if not lead.objects.filter(bot=comp.id).exists():
                serializers=lead_serilizer(data=data,partial=True) 
                if serializers.is_valid():
                    serializers.save()
                    leads=lead.objects.get(id=serializers.data['id'])
                    lead_list=[
                        lead_question(
                            lead=leads,
                            question="Name",
                            order_id=1,
                            isQuestionEditable=True,
                            lead_info_status=True,
                            filedName="Name"
                        ),
                        lead_question(
                            lead=leads,
                            question="Email",
                            order_id=2,
                            lead_info_status=True,

                            isQuestionEditable=True,
                            filedName="Email"
                        ),
                        lead_question(
                            lead=leads,
                            question="Phone Number",
                            order_id=3,
                            lead_info_status=True,
                            isQuestionEditable=True,
                            filedName="Phone"
                        )
                    ]
                    lead_question.objects.bulk_create(lead_list)
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializers.data},status=status.HTTP_200_OK)
                else:                
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error","data":serializers.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "ALready exists the lead."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)
               
    def patch(self,request):
        user=request.user
        data=request.data
        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            if lead.objects.filter(bot=comp).exists():
                lead_info=lead.objects.get(bot=comp)
                serializers=lead_serilizer(lead_info,data=data,partial=True)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializers.data},status=status.HTTP_200_OK)
                else:                
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error","data":serializers.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please check the leads."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            if lead.objects.filter(bot=comp).exists():
                lead_info=lead.objects.get(bot=comp)
                lead_info.delete()
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':''},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please check the leads."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

class Lead_Infos_API(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user=request.user
        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            if lead.objects.filter(bot=comp).exists():
                lead_=lead.objects.get(bot=comp)
                lead_info=lead_question.objects.filter(lead=lead_.id)
                serializers=lead_information_serilizer(lead_info,many=True)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializers.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the lead."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        user=request.user
        data=request.data
        if create_company.objects.filter(email=user).exists():
            comp=create_company.objects.get(email=user)
            if lead.objects.filter(bot=comp).exists():
                lead_info=lead.objects.get(bot=comp)
                data['lead']=lead_info.id
                # print(data)
                serializers=lead_information_serilizer(data=data,partial=True)
                if serializers.is_valid():
                    serializers.save()
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializers.data},status=status.HTTP_200_OK)
                else:                
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error","data":serializers.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the lead."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please create the company."},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        pk=pk
        data=request.data
        if lead_question.objects.filter(id=pk).exists():
            lead_info=lead_question.objects.get(id=pk)
            serializers=lead_information_serilizer(lead_info,data=data,partial=True)
            if serializers.is_valid():
                serializers.save()
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializers.data},status=status.HTTP_200_OK)
            else:                
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Error","data":serializers.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please check the leads information."},status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        pk=pk
        if lead_question.objects.filter(id=pk).exists():
            lead_info=lead_question.objects.get(id=pk)
            # if lead_info.isQuestionEditable:
            #     return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Question can't delete",'data':''},status=status.HTTP_200_OK)
            lead_info.delete()
            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':''},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Please check the leads information."},status=status.HTTP_400_BAD_REQUEST)

class Lead_ListAPI(APIView):
    permission_classes = (IsAuthenticated,)
    #Get All Leads
    def get(self, request):
        user=request.user
        try:
            if user:
                lead_inf=lead_information.objects.filter(user=user).order_by("-createdAt")
                # chat = chat_log.objects.filter(company=comp).exclude(recipient_id=None).values('recipient_id').distinct()
                serializer = Chatlog_List_Serializer(lead_inf,many=True)
                filtered_data = [d for d in serializer.data if d['name'] != '-' or d['phone_number'] != '-' or d['email'] != '-']
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':filtered_data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Company profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    #Get Lead Chatlog based on recipient_id
    def post(self,request):
        user=request.user
        data=request.data
        try:
            if create_company.objects.filter(email=user).exists():
                comp=create_company.objects.get(email=user)
                chat = chat_log.objects.filter(company=comp).filter(recipient_id=data['recipient_id']).order_by('id')
                serializer = Chatlog_Serializer(chat,many=True)
                return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializer.data},status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Company profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    # Patch Leads status
    def patch(self,request,pk):
        user=request.user
        pk=pk
        data=request.data
        try:
            if user and lead_information.objects.filter(id=pk).exists():
                lead_inf=lead_information.objects.get(id=pk)
                serializer = Chatlog_List_Serializer(lead_inf,data=data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':serializer.data},status=status.HTTP_200_OK)
                else:
                    return Response({'status': status.HTTP_400_BAD_REQUEST,'message': serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Company profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            lead = lead_information.objects.get(id=pk, user=request.user)
            lead.delete()
            return Response({'status': status.HTTP_200_OK, 'message': 'Lead successfully deleted.'}, status=status.HTTP_200_OK)
        except lead_information.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': 'Lead not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': str(e)},status=status.HTTP_400_BAD_REQUEST)

class lead_SortingAPI(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, format=None):
        user=request.user
        today = timezone.now().date()
        if user:
            lead_inf=lead_information.objects.filter(user=user).filter(createdAt__date=today)
            content ={
                "today_lead_count":lead_inf.count()
            } 
            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':content},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Company profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request, format=None):
        user=request.user
        data=request.data
        today = data['date']
        lead_status_data=data['status']
        if user:
            lead_inf=lead_information.objects.filter(user=user)
            if today!=None:
                lead_inf=lead_inf.filter(createdAt__date=today)
            if lead_status_data!=None:
                lead_inf=lead_inf.filter(status=lead_status_data)
            lead_inf=lead_inf.order_by("-createdAt")
            serializer = Chatlog_List_Serializer(lead_inf,many=True)
            filtered_data = [d for d in serializer.data if d['name'] != '-' or d['phone_number'] != '-' or d['email'] != '-']
            return Response({'status': status.HTTP_200_OK,'message': 'Successfully!','data':filtered_data},status=status.HTTP_200_OK)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST,'message': "Company profile doesn't exists."},status=status.HTTP_400_BAD_REQUEST)
                  
                
class Create_LeadInformationAPI(APIView):
    def post(self, request, format=None):
        data = request.data

        company_id = request.query_params.get('company', "")
        if company_id:
            try:
                company = create_company.objects.get(id=company_id)
            except create_company.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "Company details not found!"}, status=status.HTTP_400_BAD_REQUEST)

            seri = PromtData(company)
            user_seri_data = seri.data
            user_email = user_seri_data.get('email')

            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': "User not found!"}, status=status.HTTP_400_BAD_REQUEST)

            data['user'] = user.id

            if create_company.objects.filter(email=user).exists():
                comp=create_company.objects.get(email=user)
                if lead.objects.filter(bot=comp).exists():
                    lead_=lead.objects.get(bot=comp)
                    lead_info=lead_question.objects.filter(lead=lead_.id)
                    if lead_info.exists():
                        serializers = lead_information_serilizer(lead_info, many=True)
                        if serializers.data:
                             print(serializers.data[0]['question'],"------------------------------")

            
            serializer = lead_create_Serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'message': 'Successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Error!', 'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': 'Company ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
