from django.conf import settings
from random import randint
from django.template.loader import  get_template

from sendgrid import SendGridAPIClient
from Company.models import *

def generate_random_otp(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def mail_send(user,subject,ctx):
    ctx=ctx
    if template_config.objects.filter(template="2").exists():
        tmp=template_config.objects.get(template="2")
        ctx['data1']=tmp.data1
        ctx['data2']=tmp.data2
        ctx['data3']=tmp.data3
    
    message = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': user.email
                        }
                ],
                'subject': subject
                }
        ],
        'from': {
            'email': settings.SENDGRID_EMAIL
            },
        'content': [
            {
                'type': 'text/html',
                'value': get_template('OTP.html').render(ctx)
                }
        ]
    }
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)#"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")#"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")
        response = sg.send(message)
        # print(response.status_code)
        return response.status_code
    except Exception as e:
        print("error mail send",str(e))
        return False

def mail_sendforgot(user,subject,ctx):
    ctx=ctx
    if template_config.objects.filter(template="1").exists():
        tmp=template_config.objects.get(template="1")
        ctx['data1']=tmp.data1
        ctx['data2']=tmp.data2
        ctx['data3']=tmp.data3
        ctx['url_data']=tmp.url_data
    message = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': user.email
                        }
                ],
                'subject': subject
                }
        ],
        'from': {
            'email': settings.SENDGRID_EMAIL
            },
        'content': [
            {
                'type': 'text/html',
                'value': get_template('ForgotPassword.html').render(ctx)
                }
        ]
    }
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)#"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")#"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")
        response = sg.send(message)
        # print(response.status_code)
        return response.status_code
    except Exception as e:
        print("error mail send",str(e))
        return False