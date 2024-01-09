from rest_framework import serializers
from Signup.models import User
from Company.models import *

class AdminChatLogSerializer(serializers.ModelSerializer):
    company = serializers.ReadOnlyField(source='company.company')
    company_total_token = serializers.ReadOnlyField(source='company.company_total_token')
    class Meta:
        model = chat_log        
        fields = ('company_id',"company",'company_total_token','prmt','text','prm_token','used_token','total_token')

class AdminMailConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = template_config
        fields = "__all__"

class AdminUersSerializer(serializers.ModelSerializer):
    email_id = serializers.ReadOnlyField(source='id')
    company=serializers.SerializerMethodField("get_company",read_only=True)
    sales_representative_name=serializers.SerializerMethodField("get_sales_representative_name",read_only=True)
    website=serializers.SerializerMethodField("get_website",read_only=True)
    about_company=serializers.SerializerMethodField("get_about_company",read_only=True)

    class Meta:
        model = User
        fields = ('email_id','email','is_active','is_facebook','is_insta','company','sales_representative_name','website','about_company')

    def get_company(self,obj):
        if create_company.objects.filter(email=obj.id).exists():
            comp=create_company.objects.get(email=obj.id)
            # print(comp.company)
            return comp.company
        else:
            return "-"

    def get_sales_representative_name(self,obj):
        if create_company.objects.filter(email=obj.id).exists():
            comp=create_company.objects.get(email=obj.id)
            return comp.sales_representative_name
        else:
            return "-"            
    def get_website(self,obj):
        if create_company.objects.filter(email=obj.id).exists():
            comp=create_company.objects.get(email=obj.id)
            return comp.website
        else:
            return "-"

    def get_about_company(self,obj):
        if create_company.objects.filter(email=obj.id).exists():
            comp=create_company.objects.get(email=obj.id)
            return comp.about_company
        else:
            return "-"