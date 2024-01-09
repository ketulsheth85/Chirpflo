from rest_framework import serializers
from Signup.models import User
from .models import *

class CompanySerializer(serializers.ModelSerializer):
    CHATBOT_URL=serializers.SerializerMethodField("chat_got",read_only=True)
    address = serializers.CharField(allow_blank=True, allow_null=True)
    website = serializers.URLField(allow_blank=True)
    booking_link = serializers.URLField(allow_blank=True)    
    product_price = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = create_company
        fields = ('id','email','company','country',"CHATBOT_URL",'city','address','product_price','website','booking_link','about_company','is_autoresponce')

    def chat_got(self,obj):
        return f"https://chirpflo.com/testchatbot?company={obj.id}"

class CompanySerializer_Knowledge_Base(serializers.ModelSerializer):
    bot_name=serializers.CharField(source="sales_representative_name")
    class Meta:
        model = create_company
        fields = ('id','email','bot_name','tone','role','welcome_msg','name','phone_number','email_address','call_to_actions','agent_rules')

class PromtData(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='email.email')

    class Meta:
        model = create_company
        fields = ('company','country','city','address','product_price','sales_representative_name','website','booking_link','about_company','tone','email','role','name','phone_number','email_address','call_to_actions','text_information','pdf_information','agent_rules')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','is_active','is_insta','is_facebook')

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model  = chat_log
        fields = "__all__"

class Chatlog_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = chat_log
        fields = ("id","prmt","text",'recipient_id')

class Web_Ques_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = website_ques
        fields = ("user","website_url","text","prm_token","used_token","total_token")

class Ques_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = knowledge_base_ques
        fields = ("id","source","source_name","questions","answers","user")

class wellcome_serializer(serializers.ModelSerializer):
     class Meta:
         model = create_company
         fields = ('id','welcome_msg',)

class WebWidgetSerializer(serializers.ModelSerializer):
    default_launcher_icon=serializers.SerializerMethodField("get_default_icons",read_only=True)
    company=serializers.SerializerMethodField("get_company",read_only=True)

    class Meta:
        model = webchat_widget
        fields = ('id','user','chatbot_avtar','website','default_launcher_icon',"name",'bg_chatbot',"heading","sub_heading","color","background_color","client_bubble_color","text_color","bubble_text_color","status",'launcher_icon_status','launcher_icon','company','popup_status','timer_count')

    def get_default_icons(self,obj):
        if obj.default_launcher_icon==None:
            icons = dict(ICONS)
            icon=[]
            for i in icons:
                print(i)
                data={}
                data['link']=icons[i]
                data['status']=False
                icons[i]=data
                icon.append(data)
            return icon
        else:
            icons = dict(ICONS)
            active = dict(ICONS).get(obj.default_launcher_icon)
            icon=[]
            for i in icons:
                data={}
                data['link']=icons[i]
                if str(icons[i])==str(active):
                    data['status']=True
                else:
                    data['status']=False
                icons[i]=data
                icon.append(data)
            return icon

    def get_company(self,obj):
        comp=create_company.objects.get(email=obj.user.id)
        return comp.id

class WebWidgetEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = webchat_widget
        fields = ('user','bg_chatbot','chatbot_avtar','website','default_launcher_icon',"name","heading","sub_heading","status","color","background_color","client_bubble_color","text_color","bubble_text_color",'popup_status','timer_count','launcher_icon_status')

class Avtar_Image_WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = webchat_widget
        fields = ('user','chatbot_avtar')

class Icon_Image_WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = webchat_widget
        fields = ('user','launcher_icon_status','launcher_icon','js_script_file')

class Widget_Js_ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = webchat_widget
        fields = ('user','js_script_file')

class WidgetGetSerializer(serializers.ModelSerializer):
    launcher_icon=serializers.SerializerMethodField("get_default_icons",read_only=True)
    company=serializers.SerializerMethodField("get_company",read_only=True)
    background_color=serializers.SerializerMethodField("get_background",read_only=True)

    class Meta:
        model = webchat_widget
        fields = ('company',"name","heading","sub_heading",'chatbot_avtar',"launcher_icon",'website',"color","status",'popup_status','timer_count',"background_color","client_bubble_color","text_color","bubble_text_color")

    def get_default_icons(self,obj):
        if obj.launcher_icon_status:
            print(obj.launcher_icon)
            return obj.launcher_icon.url
        elif obj.default_launcher_icon!=None:
            active = dict(ICONS).get(obj.default_launcher_icon)
            return active
    
    def get_background(self,obj):
        print(obj.bg_chatbot)
        if obj.bg_chatbot:
            print(obj.bg_chatbot)
            return obj.bg_chatbot.url
        else:
            print(obj.background_color)
            return obj.background_color

    def get_company(self,obj):
        comp=create_company.objects.get(email=obj.user.id)
        return comp.id

class ChatBot_bgimage_WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = webchat_widget
        fields = ('user','bg_chatbot')

class Document_serilizer(serializers.ModelSerializer):
    class Meta:
        model = create_company
        fields = ('pdf_information','pdf_doc')

class lead_serilizer(serializers.ModelSerializer):
    class Meta:
        model = lead
        fields = ('id','bot','welcome_lead_message','lead_status','positive_lead_choice','continue_lead_choice','closing_lead_message','positive_lead_closing_choice','continue_lead_closing_choice','generate_lead_choice')

class lead_information_serilizer(serializers.ModelSerializer):
    class Meta:
        model = lead_question
        fields = ('id','lead','lead_info_status','question','order_id','isQuestionEditable','filedName')

class lead_view_serilizer(serializers.ModelSerializer):
    lead_information = serializers.SerializerMethodField()
    
    class Meta:
        model = lead
        fields = ('id','bot','welcome_lead_message','lead_status','positive_lead_choice','continue_lead_choice','closing_lead_message','positive_lead_closing_choice','continue_lead_closing_choice','lead_information','generate_lead_choice')

    def get_lead_information(self, instance):
        lead_info=lead_question.objects.filter(lead=instance).order_by("order_id")
        print(lead_info)
        return lead_information_serilizer(lead_info, many=True).data

class lead_create_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = lead_information
        fields = ('user','recipient_id','name','phone_number','email')

class Chatlog_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model  = lead_information
        fields = ("id",'recipient_id','name','phone_number','email','createdAt','status','lead_summary')