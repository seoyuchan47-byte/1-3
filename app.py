import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# 환경변수에서 Gemini API 키를 안전하게 가져옵니다.
API_KEY = os.environ.get("GEMINI_API_KEY")

if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    client = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({'error': '서버에 API 키가 설정되지 않았습니다. 환경변수를 확인해주세요!'}), 500

    user_message = request.json.get('message', '')
    if not user_message:
        return jsonify({'error': '고민 내용을 입력해주세요.'}), 400

    try:
        # 최신 gemini-2.5-flash 모델과 연애 상담가 페르소나 설정
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "당신은 다정하면서도 때로는 뼈를 때리는 20대 친근한 연애 코치 '재미나이'입니다. "
                    "사용자의 연애 고민(썸, 이별, 짝사랑 등)에 깊이 공감해주되, 친구처럼 친근한 반말로 조언해주세요. "
                    "이모지를 풍부하게 사용하고, 질질 끄는 관계에는 단호하게 팩트 폭행을 날려주세요."
                )
            )
        )
        return jsonify({'reply': response.text})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': '재미나이가 지금 다른 상담 중이라 바빠요. 잠시 후 다시 말 걸어주세요!'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
