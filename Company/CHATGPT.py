import requests
import json
from InstaGpt import settings
from .models import create_company
from .serializers import *
from datetime import datetime 
import openai
from django.db.models import Q
import time
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.callbacks import get_openai_callback
from .FAQ import *

#============================================================ CHATGPT KEY=========================================
openai.api_key=settings.OPENGPTKEY
# ============================================================ FAQ's CHAT-GPT 3.5 ================================================================================
def smsgpt_(user_data):   
    try:
        prmt=f"{user_data}.\nSummarize above content and only give in the python dictionary format key has questions and value has answer from content atleast 3."
        summ_completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",#"gpt-3.5-turbo",
            messages=[
                {"role": "system","content":prmt},
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=500,
            frequency_penalty=0,
            presence_penalty=0
        )
        return summ_completions,json.loads(summ_completions['choices'][0]['message']['content'])
    except Exception as e:
        print(str(e))
        return None,None

def exract_lead_information(conversation):   
    try:
        prmt=f"""Summarize the below conversation and write "name, email, and phone, lead_information" in JSON format.
        if do not find the above infomation write "-".
        lead_information having summary of the conversation in two or three sentence.
        {conversation}
        """
        summ_completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",#"gpt-3.5-turbo",
            messages=[
                {"role": "system","content":prmt},
            ],
            temperature=0,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        result=json.loads(summ_completions['choices'][0]['message']['content'])
        return result
    except Exception as e:
        print(str(e))
        return None


def get_faq_responce(user_input,faq_data):
    try:
        query = f"""
        Use the below knowdlegde to answer the subsequent question. 
        If the answer cannot be found, write "False".
        knowdlegde:
        \"\"\"
        {faq_data}
        \"\"\"
        Question: {user_input}"""
        summ_completions = openai.ChatCompletion.create(
            messages=[
                {'role': 'system', 'content': 'You answer questions about the knowlegde.'},
                {'role': 'user', 'content': query},
            ],
            model="gpt-3.5-turbo-16k",
            temperature=0,
        )

        return summ_completions['choices'][0]['message']['content']#summ_completions['choices'][0]['message']['content']
    except Exception as e:
        print(str(e))
        return None,None

def prmt_creations(user_data,comp,user_input):
    avoid=["company","sales_representative_name","role",'name','email_address','phone_number','call_to_actions','tone','text_information','pdf_information','agent_rules','product_price','about_company']

    company_knw=['product_price','about_company']

    company_information = preprocess('\n\n '.join(key +" : " + str(value) for key, value in user_data.items() if key not in avoid and value!=None))

    company_knowdledge ='\n\n '.join(key +" : " + str(value) for key, value in user_data.items() if key in company_knw and value!=None)

    if user_data['pdf_information']!=None:
        pdf_information=user_data['pdf_information']
    else:
        pdf_information=""
    if user_data['text_information']!=None:
        other_information=user_data['text_information']
    else:
        other_information=""

    current_date=datetime.now()
    tone_messages = {

        "funny": f"You are an extremely funny {user_data['role']} for a business in {user_data['company']} known as {user_data['sales_representative_name']}.Additionally, you should try to incorporate humor into your responses in a way that is appropriate for a professional setting.Use clever wordplay, amusing anecdotes, or witty observations but NO jokes to bring a smile to the customer's face.But remember to keep it lighthearted and respectful, and always prioritize providing helpful and informative responses.",

        "humorous": f"You are an extremely humorous {user_data['role']} for a business in {user_data['company']} known as {user_data['sales_representative_name']}.Additionally, you should try to incorporate humor into your responses in a way that is appropriate for a professional setting.Use clever wordplay, amusing anecdotes, or witty observations but NO jokes to bring a smile to the customer's face.But remember to keep it lighthearted and respectful, and always prioritize providing helpful and informative responses.",

        "sales genius": f"You are a top gun {user_data['role']} of {user_data['company']} company known as {user_data['sales_representative_name']}.Maintain a confident and persuasive demeanor like a super advanced and profesional sales person, while still being approachable and friendly.Use language that highlights the unique features and benefits of the product or service.",

        "empathetic":f"You are a {user_data['role']} of {user_data['company']} company known as {user_data['sales_representative_name']}.Avoid rushing through conversations, and take the time to fully understand the customer's situation before providing a solution.Remember to use language that is warm and welcoming.",

        "calm":f"You are a {user_data['role']} of {user_data['company']} company known as {user_data['sales_representative_name']}.Avoid rushing through conversations, and take the time to fully understand the customer's situation before providing a solution.Remember to use language that is warm and welcoming.",

        "friendly": f"You are a {user_data['role']} of {user_data['company']} company known as {user_data['sales_representative_name']}.You are always helpful and friendly.",

        "helpful": f"You are a {user_data['role']} of {user_data['company']} company known as {user_data['sales_representative_name']}.You are always helpful and friendly.",

        "mindful": f"You are a {user_data['role']} for {user_data['company']} company known as {user_data['sales_representative_name']}.It should also be engaging and relevant to the task or conversation at hand.Incorporate spiritual language, such as words of encouragement, blessings, or expressions of gratitude, to connect with customers on a deeper level. Remember to stay grounded and centered, and to approach each conversation with a sense of mindfulness and inner peace.",

        "spiritual":f"You are a {user_data['role']} of {user_data['company']} company known as {user_data['sales_representative_name']}.It should also be engaging and relevant to the task or conversation at hand.Incorporate spiritual language, such as words of encouragement, blessings, or expressions of gratitude, to connect with customers on a deeper level. Remember to stay grounded and centered, and to approach each conversation with a sense of mindfulness and inner peace.",

        "comedian":f"You are an extremely funny {user_data['role']} for a business in {user_data['company']} known as {user_data['sales_representative_name']}.\nMake them laugh with your answers it should be clear, and specific.\nTo create a hilarious customer service experience, let's try to incorporate more jokes.\nUse puns, one-liners, or funny anecdotes to make the customer laugh and feel at ease and remember, even though we're having a good time, our ultimate goal is to provide helpful and informative responses.",

    }

    tone = tone_messages.get(str(user_data['tone']).strip().lower(),"friendly")
    tone= tone+""
    kwn_data={}
    if knowledge_base_ques.objects.filter(user__email=user_data['email']).count()>0:
        kwn=knowledge_base_ques.objects.filter(user__email=user_data['email'])        
        kwn_data={chat.questions : chat.answers for chat in kwn}
        answer=""

    embeddings = OpenAIEmbeddings(openai_api_key="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",model="text-embedding-ada-002")
    # print("embeddings--------------------------------------------------------\n",embeddings)
    docs=[preprocess(company_knowdledge),preprocess(pdf_information),preprocess(other_information)]
    # print("doc--------------------------------------------------------\n",docs)

    vectorstore = FAISS.from_texts(docs, embeddings)
    retriever=vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.6})
    docs = retriever.get_relevant_documents(user_input)
    knowledge_base=[preprocess(data.page_content) for data in docs if data.page_content]

    # print("document retrieve------------------------------------------------------------------------\n",str(knowledge_base))
    if user_data['agent_rules']!=None:
        agent_rule=user_data['agent_rules'] 
    else:
        agent_rule=""

    faq_information=[(k,v) for k,v in kwn_data.items()]
    if faq_information!=[]:
        faq_information=f"Use below FAQ Information replyig related reponce:\n{faq_information}"

    else:
        faq_information=""
    
    if company_information!="":
        company_information=f"Use below Knowledge Information for replyig related reponce :\n{company_information}"
        
        if knowledge_base!=[]:
                company_information=company_information+f"\n{knowledge_base}"
    else:
        company_information=""       

    sys_pretext=None

    if lead.objects.filter(bot=comp).filter(lead_status=True).exists():
        lead_status=lead.objects.get(bot=comp)
        if lead_question.objects.filter(lead=lead_status).filter(lead_info_status=True).count()>0:
            print("================ LEAD ============================>")
            lead_ques=lead_question.objects.filter(lead=lead_status).filter(lead_info_status=True).order_by('order_id').values('question')
            leadqu=[lead_['question'] for lead_ in lead_ques]
 
            sys_pretext=f"""
            PERSONALITY:
            \"\"\"
            {tone}
            You are smart and intelligent, and you always follow the purpose and rules.
            You are not pushy at all, and helping them to determine if the product is right for them.
            You are having a conversation with a human.
            \"\"\"            
            PURPOSE :
            Your goal is to generate the next best response in the conversation to ultimately gather all of the INFORMATION TO GATHER by building trust and directing the customer towards the CALL TO ACTION.
            Your job is to qualify website visitors when they land on the site by asking them a series of questions, that will be provided to you one at a time in the INFORMATION TO GATHER, below.prioritize collecting this info.

            Welcome lead message : {lead_status.welcome_lead_message}
            Positive lead choice : {lead_status.positive_lead_choice}
            INFORMATION TO GATHER, ask one by one : {leadqu}
            CALL TO ACTION : {lead_status.closing_lead_message}
            
            {company_information}

            {faq_information}

            You're well-versed in the following rules and guidelines:
            - If user ask question/quary, responce it and moved to next question.
            - If you do not have information, write, "Unfortunately, I haven't been trained on that just yet. Please contact our support team using our email {user_data['email']} or website {user_data['website']}, and the team will be happy to assist." and Let's moved on to the next question.
            - Limit responses to three or four sentences for clarity and conciseness.
            - {agent_rule}

            Current date and time: {current_date}
            
            Always make this in the voice of {user_data['sales_representative_name']}.
            """
        else:
            pass

    if sys_pretext==None:
        # print("------------------------------------------------------2. Normal Bot-------------")
        sys_pretext=f"""
                PERSONALITY :
                \"\"\"
                {tone}
                You are smart and intelligent.
                You have a nice personality and are having a conversation with a human.
                You are not pushy at all.
                \"\"\"
                Use the below knowledge information for replying to related responses:
                {company_information}
                {knowledge_base}

                Use the below faq information for replying related response, don't hallucinate the response: 
                {[(k,v) for k,v in kwn_data.items()]}                

                You're well-versed in following the agent's rules and guidelines:
                Limit responses to three or four sentences for clarity and conciseness.
                {agent_rule}
                 
                If do not know the answer, write "Unfortunately i haven't been trained on that just yet.Please contact to our support team using our email : {user_data['email']} or website : {user_data['website']} and the team will be happy to assist".
                You always act in the same way as stated in prior instructions.
                Current date : {current_date}
                Always make this in the voice of {user_data['sales_representative_name']}.
            """
    

    # print("------------------------------------- system prompt-----------------------------------------",sys_pretext)

    return sys_pretext

def CHAT_GPT_RESPONCE(data,user_data,comp,type,receip_id):
    # -------------------------initialze prompt message
    sys_pretext=prmt_creations(user_data,comp,data['prompt'])
    sys_pretext=sys_pretext+"\n{history}\nHuman: {human_input}\n+"+f"{user_data['sales_representative_name']} :"
    
    # -------------------------initialize memory
    print("-------------------------initialize memory")
    memory=ConversationBufferWindowMemory(k=conversation_memory.objects.filter(user__email=user_data['email'],conversation_type=type).order_by("id").values().count()+1,return_messages=False,ai_prefix=user_data['sales_representative_name'])    
    user_chat=conversation_memory.objects.filter(user__email=user_data['email'],conversation_type=type).order_by("id").values()

    # ------------------------- Lead flow
    if lead.objects.filter(bot=comp).filter(lead_status=True).exists():
        lead_status=lead.objects.get(bot=comp)
        if data['prompt']==lead_status.positive_lead_choice:
            if lead_question.objects.filter(lead=lead_status).filter(lead_info_status=True).count()>0:
                print("---------------------------- Truee")
                # ------------------------ assign message in bot
                memory.save_context({"input": lead_status.welcome_lead_message}, {"output": data['prompt']})
                # ------------------------ create lead
                user=User.objects.get(email=user_data['email'])
                if not lead_information.objects.filter(user=user,recipient_id=receip_id).exists():
                    lead_information.objects.create(user=user,recipient_id=receip_id)

    # -------------------------assign memory
    for d in user_chat:
        memory.save_context({"input": d['message']}, {"output": d['responce']})


    # -------------------------prompt template 
    prompt = PromptTemplate(
        input_variables=["history","human_input"],
        template=sys_pretext
    )

    # ------------------------ initialize bot chain 
    

    chatgpt_chain = LLMChain(    
        llm=OpenAI(temperature=0,openai_api_key="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",model_name='gpt-3.5-turbo-16k'),
        prompt=prompt,
        verbose=True,
        memory=memory,
    )
    text_data=chatgpt_chain.predict(human_input=data['prompt'])
    responce=text_data
    completion=0

    # ------------------------ initialize bot cost
    with get_openai_callback() as cb:
        completion=cb
    
    # ------------------------ convert long responce to short 
    if len(text_data.split()) >= 50:
        text_data = responce
        if len(text_data.split(". "))>2:
            text_data=[". ".join(i for i in text_data.split(". ")[:round(len(text_data.split(". "))/2)])+".", ". ".join(i for i in text_data.split(". ")[round(len(text_data.split(". "))/2):])]
        else:
            text_data=[text_data]
    else:
        text_data=[text_data]

    return completion,responce,text_data

def CHAT_RESPONCE(data,user_data,comp,type,receip_id):
    print("-----------GPT",receip_id)
    try:
        input_question = data['prompt']
        print("------------------------------------------------------------------------1 count: ",conversation_memory.objects.filter(user__email=user_data['email'],conversation_type=type).count())
        #==================== CHATGPT 3.5 Responce
        completions,responce,text_data= CHAT_GPT_RESPONCE(data,user_data,comp,type,receip_id)

        user_data={
            "company":comp.id,
            "prmt":data['prompt'],
            "text":text_data or "",
            "prm_token":00,
            "used_token": 00,
            "total_token": 00,
            "recipient_id":None,
            "sender_id":None            
            }
        return user_data,responce

    except Exception as e:
        print(str(e))
        user_data={
            "company":comp.id,
            "prmt":data['prompt'],
            "text":None,
            "prm_token":00,
            "used_token":00,
            "total_token":00,
            "recipient_id":None,
            "sender_id":None
        }
        return user_data

#============================================================ Facebook user GET API =========================================

def facebook_user_get_accounts(token):
    try:
        events_task=requests.get(f'https://graph.facebook.com/v16.0/me/accounts?access_token={token}')
        # print("-->>",events_task.json())
        return events_task.json()
    except Exception as e:
        print("EXCEPTION-->", str(e))
        return str(e)

#============================================================ Through Facebook page get insta user GET API =========================================

def facebook_user_get_insta_accounts(token):
    try:
        params = {
            'fields': 'instagram_business_account,connected_instagram_account,is_webhooks_subscribed,instagram_accounts{id,username}',
            'access_token': token,
        }
        events_task=requests.get(f'https://graph.facebook.com/v16.0/me',params=params)
        return events_task.json()
    except Exception as e:
        print("EXCEPTION-->", str(e))
        return str(e)

#============================================================ Through Facebook Subscribe webhook of Meta App webhook API =========================================

def facebook_page_subcribe_app(token,page_id):
    try:
        params = {
        'subscribed_fields': 'messages',
        'access_token': token,
        }
        response = requests.post(f'https://graph.facebook.com/v16.0/{page_id}/subscribed_apps', params=params)
        return response.json()
    except Exception as e:
        print("EXCEPTION-->", str(e))
        return str(e)

#============================================================ INSTA DM API =========================================

def insta_dm(sender_id,msg,page_token):
    new_event={
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": msg
        }
    }
    headers = {
        'Content-Type':'application/json',
    }
    try:
        events_task=requests.post(f'https://graph.facebook.com/v16.0/me/messages?access_token={page_token}',
                    headers=headers,
                    data=json.dumps(new_event))
        return events_task.json()
    except Exception as e:
        print("EXCEPTION create task", str(e))
        return str(e)

#============================================================ INSTA DM API =========================================
def get_all_user_insta_dm(fields,page_token):
    params = {
            'access_token': page_token,
        }
    try:
        # fields='name,participants,messages{message,from,to}'
        events_task=requests.get(f'https://graph.facebook.com/v16.0/me/conversations?fields={fields}&platform=instagram',params=params,#EAARhKhbm7WYBAGf34aoEadZCxz71NcUKfZCeVHfft7LUl62bitBkaJLtLSsOHGZCaFkDE1cHt6rwxBMEzBM7k23gPZBZC8VDj2kPyimaasnoCfrO4aQgeEZAhEgRguGWXwud0Umoz0AJc1r3Vff7cPOHvAYl9TGbzOQvBbLIlmARGvvnZAgZBGmD',
        )
        return events_task.json()
    except Exception as e:
        print("EXCEPTION create task", str(e))
        return str(e)

def get_user_insta_profile_dm(insta_id,page_token):

    params = {
            'access_token': page_token,
        }
    try:
        events_task=requests.get(f'https://graph.facebook.com/v16.0/{insta_id}?fields=profile_pic,is_verified_user,follower_count,is_user_follow_business,is_business_follow_user',params=params,#EAARhKhbm7WYBAGf34aoEadZCxz71NcUKfZCeVHfft7LUl62bitBkaJLtLSsOHGZCaFkDE1cHt6rwxBMEzBM7k23gPZBZC8VDj2kPyimaasnoCfrO4aQgeEZAhEgRguGWXwud0Umoz0AJc1r3Vff7cPOHvAYl9TGbzOQvBbLIlmARGvvnZAgZBGmD',
        )
        return events_task.json()
    except Exception as e:
        print("EXCEPTION create task", str(e))
        return str(e)

def get_insta_messages(id,page_token):

    params = {
            'access_token': page_token,
        }
    try:
        events_task=requests.get(f'https://graph.facebook.com/v16.0/{id}'+'?fields=messages{message,from,to}',params=params,#EAARhKhbm7WYBAGf34aoEadZCxz71NcUKfZCeVHfft7LUl62bitBkaJLtLSsOHGZCaFkDE1cHt6rwxBMEzBM7k23gPZBZC8VDj2kPyimaasnoCfrO4aQgeEZAhEgRguGWXwud0Umoz0AJc1r3Vff7cPOHvAYl9TGbzOQvBbLIlmARGvvnZAgZBGmD',
        )
        return events_task.json()
    except Exception as e:
        print("EXCEPTION create task", str(e))
        return str(e)