import logging
from Company.models import *
from Company.serializers import *
from Company.CHATGPT import smsgpt_
from time import sleep
from celery import shared_task

from Company.CHATGPT import *
from bs4 import BeautifulSoup
import requests
import time
from .celery import app

@app.task
def faq_questions_task(user,urls,process):
    i=0
    error=[]
    user=User.objects.get(email=user)
    process = MyLongProcess.objects.get(active_uuid=process)
    for url in urls:
        print(process.id)
        process.current_step += 1
        process.save()
        try:
            url=str(url).strip()
            # response = requests.head(url)
            USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
            headers = {"user-agent": USER_AGENT}
            response = requests.get(url, headers=headers)
            sleep(2)

            # print(response.status_code)
            if response.status_code == 200:
                if knowledge_base_ques.objects.filter(user=user).exclude(source="3").count()>=150:
                    error.append(f"The FAQ has reached 150 questions limit!")
                    break
                # reqs = requests.get(url)
                soup = BeautifulSoup(response.content,features="html.parser")
                text = soup.get_text()

                text=list(filter(None,[chunk for chunk in text.splitlines()]))
                text=''.join(chunk for chunk in text if chunk!=" ")[:8000]
                if not website_ques.objects.filter(user=user).filter(website_url=url).exists():
                    serializer = Web_Ques_Serializer(
                        data={
                                "user":user.id,
                                "website_url":url.strip(),
                                "text":text,
                                "prm_token": 00, 
                                "used_token":00, 
                                "total_token":00,
                            }
                    )
                    if serializer.is_valid():
                        serializer.save()
                        web_data=serializer.data
                        print("data created and  saved")
                    else:
                        error.append(f"{serializer.errors}")
                else:
                    web=website_ques.objects.get(website_url=url)
                    serializer = Web_Ques_Serializer(
                        web,data={
                            "user":user.id,
                            "website_url":url.strip(),
                            "text":text,
                            "prm_token": 00,
                            "used_token":00,
                            "total_token": 00,
                        }
                        ,partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        web_data=serializer.data
                        print("data updated and  saved")
                    else:
                        error.append(f"{serializer.errors}")
                        pass
                if web_data:
                    gtp_data, questions=smsgpt_(web_data['text'])
                    if questions==None:
                        error.append(f"{gtp_data}")
                        pass
                    else:
                        question_=[]
                        for key,value in questions.items():
                            if knowledge_base_ques.objects.filter(user=user).filter(source="2").filter(questions=key).exists():
                                pass
                            else:
                                question_.append(knowledge_base_ques(
                                    user=user,
                                    source=2,
                                    source_name=web_data['website_url'],
                                    questions=key,
                                    answers=value
                                ))
                        try:
                            knowledge_base_ques.objects.bulk_create(question_)
                            logger = logging.getLogger("info")
                            logger.info("Test4")
                            del question_
                            process.success+=1
                            process.save()

                        except Exception as e:
                            error.append(f"{e}")
                            pass
                else:
                    error.append(f"Data Not Found")
                    pass
            else:
                error.append(f"{url}")
                pass
        except Exception as e:
            error.append(f"{url}")

    if error!=[]:
        return str(error)
    else:
        return "Successfully"

# @app.task(serializer='json')
# def pdf_faq_quesition_task(user,pdf_data,name,process):
#         error=[]
#         try:
#             pdf_data=pdf_data
#             user=User.objects.get(email=user)
#             process = MyLongProcess.objects.get(active_uuid=process)
#             for page_data in pdf_data:
#                 print(process.id)
#                 process.current_step += 1
#                 text = page_data
#                 # text=list(filter(None,[chunk for chunk in text]))
#                 # text=''.join(chunk for chunk in text if chunk!=" ")
#                 gtp_data, questions=smsgpt_(text)
#                 if questions==None:
#                     error.append(f"{gtp_data}")
#                 else:
#                     question_=[]
#                     for key,value in questions.items():
#                         if knowledge_base_ques.objects.filter(user=user).filter(source="2").filter(questions=key).exists():
#                             pass
#                         else:
#                             question_.append(knowledge_base_ques(
#                                 user=user,
#                                 source=2,
#                                 source_name=name,
#                                 questions=key,
#                                 answers=value
#                             ))
#                     try:
#                         knowledge_base_ques.objects.bulk_create(question_)
#                         del question_
#                         process.success+=1
#                         process.save()
#                     except Exception as e:
#                         error.append(f"{e}")

#         except Exception as e:
#             error.append(f"{e}")

#         if error!=[]:
#             return str(error)
#         else:
#             return "Successfully"


