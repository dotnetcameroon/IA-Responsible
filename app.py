import os
from flask import Flask, request, render_template
from dotenv import load_dotenv
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import TextCategory
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions

app = Flask (__name__)
load_dotenv()
key = os.getenv("API")
endpoint = os.getenv("ENPOINT")

client=ContentSafetyClient(endpoint,AzureKeyCredential(key))

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        text_content = request.form['text_content']
        result = analyze_text(text_content)
        return render_template('index.html',result=result,text_content=text_content)
    return render_template ('index.html')

def analyze_text(text_content):
    request = AnalyzeTextOptions (text=text_content)
    try
