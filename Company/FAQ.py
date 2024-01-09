from .models import *
from .serializers import *
from .CHATGPT import *

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# import openai
# openai.api_key=settings.OPENGPTKEY
# Preprocess the questions
stop_words = set(stopwords.words("english"))
def preprocess(text):
    tokens = word_tokenize(text.lower())
    filtered_tokens = [word for word in tokens if word not in stop_words]
    if filtered_tokens==['?']:
        filtered_tokens = [word for word in tokens]
    return " ".join(filtered_tokens)