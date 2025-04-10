from flask import Flask, render_template, request, jsonify 
import random
import time 
import json
import os 
from openai import OpenAI
import requests 

client = OpenAI(
    api_key='sk-660aad31403d4a87b5ee1e790baf8013',
    base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)


def get_llm_response(prompt):
    try:
        response = client.chat.completions.create(
            model="qwen-max",
            messages=[
            {"role": "system", "content": "You are Lydia, a Multilingual Tour Guide, fluent in multiple languages and capable of switching smoothly between them based on guest preferences. Your primary purpose is to lead immersive, culturally rich tours that feel personal, exciting, and easy to follow—no matter the language."},
            {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling Qwen API: {str(e)}")
        return "I'm sorry, I'm having trouble processing your request right now."

app = Flask(__name__)

@app.route('/')
def index():
    vercel_url="https://wander-bot-alibaba.vercel.app/"
    return render_template('index.html', vercel_url=vercel_url) 

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"response": "Please enter a message."})
    
    response = get_llm_response(user_message)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)