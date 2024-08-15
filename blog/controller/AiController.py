from langchain_community.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings  # تأكد من استيراد نموذج التضمين المناسب
from blog import cfg
from flask import jsonify, request, render_template, url_for
import requests

import random

class AiController:
    
    # without langchin
    def get_orign_gbt_request():
        try:
            user_input = request.json["message"] # إدخال المستخدم
        except:
            return jsonify({"message":"no send masage"})

        # إعداد عنوان URL للواجهة
        url = 'https://api.openai.com/v1/chat/completions'

        # إعداد رأس الطلب
        headers = {
            'Authorization': f'Bearer {cfg.OPENAI_API_KEY}',
            'Content-Type': 'application/json',
        }

        # إعداد جسم الطلب
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'user', 'content': user_input}
            ],
            'max_tokens': 50
        }

        # إرسال الطلب
        response = requests.post(url, headers=headers, json=data)

        # عرض استجابة الواجهة
        if response.status_code == 200:
            result = response.json()
            return jsonify({"message":result['choices'][0]['message']['content']})
        else:
            return jsonify({"message":f"Error: {response.status_code}"})
    
    # with langchin
    def get_gbt_request():
        try:
            user_input = request.json["message"] # إدخال المستخدم
        except:
            return jsonify({"message":"no send masage"})
        loader = TextLoader(r"C:\Users\alshi\OneDrive\سطح المكتب\مؤقت\ai_blog\blog\static\files\data.txt", encoding="utf-8") # تحميل البيانات من الملف
        # تحديد نموذج التضمين
        embedding_model = OpenAIEmbeddings(api_key=cfg.OPENAI_API_KEY)  # يمكنك تغيير هذا إلى نموذج مناسب لك
        index_creator = VectorstoreIndexCreator(embedding=embedding_model)# إنشاء فهرس من البيانات المحملة
        index = index_creator.from_loaders([loader])
        response = index.query(question=user_input, llm=ChatOpenAI()) # استعلام الفهرس
        

        # إنشاء فهرس باستخدام Faiss
        # index_creator = VectorstoreIndexCreator(vectorstore=Faiss())

        return jsonify({"message":response})
    
    
    def gbt_page():
        global URL_KEY
        URL_KEY = str(random.randint(100_000_000, 999_999_999))
        return render_template('gbt.jinja', title="مهند", URL_KEY= URL_KEY)