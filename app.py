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
    request = AnalyzeTextOptions(text=text_content)
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        return {"error": f"Analyze text failed. Error code: {e.error.code}, Error message: {e.error.message}"}

    results = {
        "Hate severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.HATE), 0),
        "SelfHarm severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SELF_HARM), 0),
        "Sexual severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.SEXUAL), 0),
        "Violence severity": next((item.severity for item in response.categories_analysis if item.category == TextCategory.VIOLENCE), 0)
    }

    conclusion = []
    for category, severity in results.items():
        if severity >= 4:
            conclusion.append(f"{category} severity")

    results["Conclusion"] = ", ".join(conclusion) if conclusion else "No high severity content detected."
    return results


if __name__ == "__main__":
    app.run(debug=True)