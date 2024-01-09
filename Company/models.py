from django.db import models
from Signup.models import User
from InstaGpt.storage_backend import *
# Create your models here.
class create_company(models.Model):
    email = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    company = models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=100,null=True,blank=True)
    product_price=models.TextField(null=True)
    sales_representative_name = models.CharField(max_length=100,null=True,blank=True)
    website = models.URLField(max_length=100,null=True,blank=True)
    booking_link = models.URLField(max_length=100,null=True,blank=True)
    about_company = models.TextField(null=True,blank=True)
    prmt=models.TextField(default="",null=True,blank=True)
    is_autoresponce=models.BooleanField(default=False)
    address=models.TextField(null=True)
    city=models.CharField(max_length=100,null=True,blank=True,default=None)
    bussiness_hour=models.JSONField(null=True, blank=True)
    contact_us=models.BigIntegerField(null=True,blank=True)
    welcome_msg=models.CharField(max_length=250,blank=True,null=True)
    createdAt = models.DateField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateField(auto_now=True)
    facebook_page_id=models.BigIntegerField(null=True,blank=True)
    facebook_page_access_token=models.CharField(max_length=400,null=True,blank=True)
    facebook_page_access_token_expire_time=models.DateField(null=True, blank=True)
    facebook_user_access_token=models.CharField(max_length=400,null=True,blank=True)
    tone=models.CharField(max_length=100,null=True,blank=True)
    role=models.CharField(max_length=100,default=None,blank=True,null=True)
    company_total_token=models.IntegerField(default=None,blank=True,null=True)
    name = models.BooleanField(default=False)
    phone_number = models.BooleanField(default=False)
    email_address = models.BooleanField(default=False)
    call_to_actions=models.CharField(max_length=250,blank=True,null=True)
    text_information=models.TextField(null=True,blank=True)
    agent_rules=models.TextField(null=True,blank=True)
    pdf_information=models.TextField(null=True,blank=True)
    pdf_doc = models.FileField(storage=ProfileMediaStorage(), null=True, blank=True, default=None)

    def __str__(self):
        return self.company

class website_ques(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    website_url = models.URLField(max_length=100,null=True,blank=True)
    text = models.TextField(default="",null=True,blank=True)
    prm_token=models.IntegerField()
    used_token=models.IntegerField()
    total_token=models.IntegerField()
    createdAt = models.DateField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateField(auto_now=True)
    def __str__(self):
        return self.website_url

TYPE_KW=(
    ('1', 'company'), 
    ('2','website'),
    ('3','live mesasges')
)

class knowledge_base_ques(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    source = models.CharField(max_length=200,choices=TYPE_KW,null=True,blank=True)
    source_name = models.CharField(max_length=200,null=True,blank=True)
    questions=models.CharField(max_length=500,default=None,blank=True,null=True)
    answers=models.CharField(max_length=500,default=None,blank=True,null=True)
    createdAt = models.DateField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateField(auto_now=True)
    def __str__(self):
        return self.questions

class chat_log(models.Model):
    company = models.ForeignKey(create_company, on_delete=models.CASCADE)
    prmt=models.TextField(default="",null=True,blank=True)
    text = models.TextField(default="",null=True,blank=True)
    prm_token=models.IntegerField()
    used_token=models.IntegerField()
    total_token=models.IntegerField()
    is_responce=models.BooleanField(default=False,null=True,blank=True)
    sender_id=models.BigIntegerField(null=True,blank=True)
    recipient_id=models.BigIntegerField(null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.prmt

TYPE_CONV=(
    ('1', 'company-based'), 
    ('2','login-based'),
    ('3','social'),
)

class conversation_memory(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    conversation_type = models.CharField(max_length=200,choices=TYPE_CONV,null=True,blank=True)
    sender_id=models.BigIntegerField(null=True,blank=True)
    recipient_id=models.BigIntegerField(null=True,blank=True)
    message=models.TextField(default="",null=True,blank=True)
    responce = models.TextField(default="",null=True,blank=True)
    is_responce=models.BooleanField(default=False,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"user:{self.user} sender:{self.sender_id}"

TEMPLATE = (
    ('1', 'forgot_password'), 
    ('2','otp')
)

class template_config(models.Model):
    template = models.CharField(max_length=200,choices=TEMPLATE,null=True,blank=True)
    data1 = models.CharField(max_length=200,null=True,blank=True)
    data2 = models.CharField(max_length=200,null=True,blank=True)
    data3 = models.CharField(max_length=200,null=True,blank=True)
    url_data= models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.template

class MyLongProcess(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    active_uuid = models.UUIDField('Active process', null=True, blank=True)
    name = models.CharField('Name', max_length=255)
    current_step = models.IntegerField('Current step', default=0)
    total = models.IntegerField('Total', default=0)
    success = models.IntegerField('Success', default=0)

    @property
    def percentage_sending(self):
        # or it can be computed by filtering elements processed in celery with complete status
        return int((self.current_step / self.total) * 100)

    def __str__(self):
        return str(self.active_uuid)

from InstaGpt.storage_backend import *
ICONS = (
    ('1','https://chatgpts.s3.us-west-2.amazonaws.com/chatlogo/chat-message.svg'), 
    ('2','https://chatgpts.s3.us-west-2.amazonaws.com/chatlogo/chatlauncher-icon.svg'),
    ('3','https://chatgpts.s3.us-west-2.amazonaws.com/chatlogo/tabler_message-chatbot.svg'), 
    ('4','https://chatgpts.s3.us-west-2.amazonaws.com/chatlogo/user-icon.svg')
)


class webchat_widget(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=200,null=True,blank=True)
    heading = models.CharField(max_length=200,null=True,blank=True)
    sub_heading = models.CharField(max_length=200,null=True,blank=True)
    status=models.BooleanField(default=False,null=True,blank=True)
    popup_status=models.BooleanField(default=False,null=True,blank=True)
    timer_count=models.IntegerField(default=0,blank=True,null=True)
    chatbot_avtar = models.FileField(storage=ProfileMediaStorage(), null=True, blank=True, default="default_avtar_icon_chatgpt_bucket_media.svg")
    website = models.URLField(max_length=100,null=True,blank=True)
    color = models.CharField(max_length=200,null=True,blank=True)
    background_color = models.CharField(max_length=200,null=True,blank=True)
    text_color = models.CharField(max_length=200,null=True,blank=True)
    bubble_text_color = models.CharField(max_length=200,null=True,blank=True)
    client_bubble_color = models.CharField(max_length=200,null=True,blank=True)
    default_launcher_icon = models.CharField(max_length=200,choices=ICONS,null=True, blank=True,default=None)
    launcher_icon_status=models.BooleanField(default=False,null=True,blank=True)
    launcher_icon = models.FileField(storage=ProfileMediaStorage(), null=True, blank=True, default=None)
    js_script_file = models.FileField(storage=ProfileMediaStorage(), null=True, blank=True, default=None)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)
    bg_chatbot = models.FileField(storage=ProfileMediaStorage(), null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.name}"

class lead(models.Model):
    bot = models.ForeignKey(create_company, on_delete=models.DO_NOTHING)
    welcome_lead_message=models.CharField(max_length=250,blank=True,null=True)
    lead_status=models.BooleanField(default=False)
    positive_lead_choice=models.CharField(max_length=250,blank=True,null=True)
    continue_lead_choice=models.CharField(max_length=250,blank=True,null=True)
    closing_lead_message=models.CharField(max_length=250,blank=True,null=True)
    positive_lead_closing_choice=models.CharField(max_length=250,blank=True,null=True)
    continue_lead_closing_choice=models.CharField(max_length=250,blank=True,null=True)
    generate_lead_choice=models.CharField(max_length=250,blank=True,null=True)

    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bot}"

class lead_question(models.Model):
    lead = models.ForeignKey(lead, related_name='lead_information', on_delete=models.CASCADE)
    lead_info_status=models.BooleanField(default=False)
    filedName=models.CharField(default=None,max_length=200,null=True,blank=True)
    isQuestionEditable=models.BooleanField(default=False)
    question = models.CharField(max_length=200,null=True,blank=True)
    answer = models.CharField(max_length=200,null=True,blank=True)
    order_id=models.IntegerField(default=None,null=True,blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question}"

LEAD_STATE = (
    ('1','COMPLETED'), 
    ('2','DECLINED'),
    ('3','FOLLOW UP'), 
    ('4','PENDING')
)

class lead_information(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    recipient_id=models.BigIntegerField(null=True,blank=True)
    name=models.CharField(default=None,max_length=200,null=True,blank=True)
    phone_number=models.CharField(default=None,max_length=200,null=True,blank=True)
    email=models.CharField(default=None,max_length=200,null=True,blank=True)
    status=models.CharField(max_length=200,choices=LEAD_STATE,null=True, blank=True,default="4")
    lead_summary=models.TextField(null=True,blank=True,default=None)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.recipient_id}"


