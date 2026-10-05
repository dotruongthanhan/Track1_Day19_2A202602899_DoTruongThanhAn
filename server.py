#!/usr/bin/env python3
"""
Local AI Server for Course Learning App
Loads Gemini API Key from .env and proxies synthesis and chat requests to Google Gemini Flash API.
Runs with zero external dependencies (Python 3 standard library only).
NO LENGTH LIMITS: maxOutputTokens set to 8192 (full Gemini capacity).
"""

import os
import sys
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Simple .env loader without third-party dependencies
def load_env_file(filepath='.env'):
    env_vars = {}
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    env_vars[key] = val
                    os.environ[key] = val
    # Automatically synchronize env.js for direct file:// access
    try:
        with open('env.js', 'w', encoding='utf-8') as js_file:
            js_file.write('// Auto-generated from .env (ignored by git)\n')
            js_file.write(f'window.__ENV = {json.dumps(env_vars, ensure_ascii=False)};\n')
    except Exception as e:
        pass
    return env_vars

# Load .env
ENV = load_env_file()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '').strip()
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.5-flash-lite').strip()
PORT = int(os.getenv('PORT', '8000'))

SYNTHESIS_SYSTEM_PROMPT = """Bạn là trợ lý học tập AI chuyên sâu, thông thái và tận tâm. 
Người học vừa hoàn thành hoặc đang chuẩn bị chuyển tiếp giữa các phần trong bài giảng. 
Họ đã ghi chú (take-notes) và bôi đen một số đoạn văn bản quan trọng (highlights).

Nhiệm vụ của bạn là dựa HOÀN TOÀN vào tài liệu gốc (toàn văn PDF text hoặc Markdown) để:
1. ĐIỀN TIẾP VÀ HOÀN THIỆN ĐẦY ĐỦ CÁC Ý GHI CHÚ (Take-notes):
   - Đọc các gạch đầu dòng ghi chú ngắn/dang dở của người học.
   - Đối chiếu với tài liệu gốc để bổ sung chi tiết, phân tích bản chất và mở rộng thành các bullet points mạch lạc, sâu sắc, toàn diện.
2. GIẢI THÍCH CHI TIẾT TỪNG PHẦN HIGHLIGHT:
   - Với từng đoạn văn bản hoặc từ khóa người học đã highlight, giải thích cặn kẽ: Tại sao điều này quan trọng? Bối cảnh trong bài giảng là gì? Ý nghĩa, bài học và ví dụ áp dụng thực tế?
   - Phân tích thấu đáo, rõ ràng, không cắt ngắn.
3. ĐÚC KẾT BÀI HỌC CỐT LÕI (Key Takeaways):
   - Tổng hợp bức tranh toàn cảnh để người học khắc sâu kiến thức trước khi sang phần tiếp theo.

Định dạng yêu cầu:
- Trình bày hoàn toàn bằng tiếng Việt tự nhiên, chuẩn mực, giàu tính sư phạm.
- Sử dụng định dạng Markdown rõ ràng: dùng heading ###, bullet points (- hoặc *), in đậm **khái niệm quan trọng**.
- TUYỆT ĐỐI KHÔNG CẮT NGẮN, không giới hạn độ dài câu trả lời, hãy trình bày đầy đủ toàn bộ nội dung.
"""

CHAT_SYSTEM_PROMPT = """Bạn là trợ lý học tập AI thông thái, tận tâm và chuyên sâu cho khoá học AI Product.
Người học đang đặt câu hỏi về bài giảng hoặc muốn đào sâu một vấn đề.

Nhiệm vụ của bạn:
- Dựa vào tài liệu bài học được cung cấp (toàn văn PDF Slide hoặc Markdown), hãy giải đáp câu hỏi của người học một cách ĐẦY ĐỦ, TOÀN DIỆN, CHI TIẾT và SÂU SẮC nhất.
- Nêu rõ nguyên lý cốt lõi, bối cảnh bài giảng, các bước áp dụng và ví dụ thực tế liên hệ từ bài giảng.
- TUYỆT ĐỐI KHÔNG CẮT NGẮN, không tóm tắt sơ sài. Hãy phân tích thấu đáo mọi khía cạnh của vấn đề.
- Trình bày bằng tiếng Việt chuẩn xác, sử dụng định dạng Markdown rõ ràng (tiêu đề, gạch đầu dòng, từ khóa in đậm).
"""

class AIAppHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/config':
            has_key = bool(GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            resp = {
                'hasApiKey': has_key,
                'model': GEMINI_MODEL,
                'port': PORT
            }
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return

        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        try:
            data = json.loads(body)
        except Exception as e:
            self.send_error_json(400, f'Invalid JSON payload: {str(e)}')
            return

        client_api_key = data.get('apiKey', '').strip()
        active_api_key = GEMINI_API_KEY
        if not active_api_key or active_api_key == 'your_gemini_api_key_here':
            if client_api_key:
                active_api_key = client_api_key
            else:
                self.send_error_json(400, 'Chưa có GEMINI_API_KEY trong file .env. Vui lòng thêm API Key vào file .env.')
                return

        raw_model = data.get('model', GEMINI_MODEL) or 'gemini-3.5-flash-lite'
        active_model = raw_model

        lesson = data.get('lesson', 'pdf')
        full_text = data.get('fullText', '')
        lesson_title = '1. Tư duy product (PDF Slide)' if lesson == 'pdf' else '2. MCP Multi Agent (Markdown)'

        # Endpoint 1: POST /api/synthesize (Tổng hợp kiến thức)
        if self.path == '/api/synthesize':
            notes = data.get('notes', '')
            highlights = data.get('highlights', [])

            user_content = f"""TÀI LIỆU GỐC ({lesson_title}):
\"\"\"
{full_text}
\"\"\"

CÁC ĐOẠN NGƯỜI HỌC ĐÃ HIGHLIGHT:
{chr(10).join(f"- {h}" for h in highlights) if highlights else "(Chưa có highlight cụ thể)"}

GHI CHÚ CỦA NGƯỜI HỌC (TAKE-NOTES):
{notes if notes.strip() else "(Chưa có ghi chú cụ thể)"}

YÊU CẦU:
Hãy giúp người học hoàn thiện toàn bộ các bullet point ghi chú, giải thích chi tiết, đầy đủ tất cả các đoạn highlight trên dựa vào tài liệu gốc, và đúc kết các bài học quan trọng nhất. Trả lời chi tiết, không cắt ngắn.
"""
            self.call_gemini_api(active_api_key, active_model, SYNTHESIS_SYSTEM_PROMPT, user_content)
            return

        # Endpoint 2: POST /api/chat (Hỏi đáp tự do không giới hạn với AI)
        elif self.path == '/api/chat':
            query = data.get('query', '')
            notes = data.get('notes', '')
            highlights = data.get('highlights', [])

            user_content = f"""TÀI LIỆU BÀI HỌC ({lesson_title}):
\"\"\"
{full_text}
\"\"\"

THÔNG TIN HỌC TẬP CỦA NGƯỜI DÙNG:
- Ghi chú: {notes if notes.strip() else "(Không có)"}
- Các điểm đã highlight: {', '.join(highlights) if highlights else "(Không có)"}

CÂU HỎI CỦA NGƯỜI HỌC:
"{query}"

YÊU CẦU:
Dựa vào tài liệu bài học, hãy giải thích cặn kẽ, đầy đủ, chi tiết và toàn diện nhất cho người học. Trả lời trọn vẹn, không giới hạn độ dài.
"""
            self.call_gemini_api(active_api_key, active_model, CHAT_SYSTEM_PROMPT, user_content)
            return

        self.send_error(404, "Endpoint not found")

    def call_gemini_api(self, api_key, model, system_prompt, user_content):
        # Candidate models list starting with requested model (excluding deprecated 1.5)
        candidate_models = [model, 'gemini-3.5-flash-lite', 'gemini-3.5-flash', 'gemini-3.8-flash', 'gemini-2.5-flash', 'gemini-2.0-flash']
        models_to_try = []
        for m in candidate_models:
            if m and m not in models_to_try:
                models_to_try.append(m)

        last_error = None
        for m in models_to_try:
            gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"

            payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [{"text": user_content}]
                    }
                ],
                "systemInstruction": {
                    "parts": [{"text": system_prompt}]
                },
                "generationConfig": {
                    "temperature": 0.4,
                    "maxOutputTokens": 8192  # FULL CAPACITY: GỠ TOÀN BỘ GIỚI HẠN
                }
            }

            try:
                req_data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(
                    gemini_url,
                    data=req_data,
                    headers={'Content-Type': 'application/json; charset=utf-8'},
                    method='POST'
                )

                with urllib.request.urlopen(req, timeout=90) as response:
                    res_body = response.read().decode('utf-8')
                    gemini_res = json.loads(res_body)

                candidates = gemini_res.get('candidates', [])
                if not candidates:
                    continue

                content_parts = candidates[0].get('content', {}).get('parts', [])
                reply_text = "".join(part.get('text', '') for part in content_parts)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'reply': reply_text,
                    'synthesis': reply_text,
                    'model': m
                }, ensure_ascii=False).encode('utf-8'))
                return

            except urllib.error.HTTPError as he:
                err_content = he.read().decode('utf-8', errors='ignore')
                err_msg = f"Lỗi từ Gemini API (HTTP {he.code}): {err_content}"
                last_error = err_msg
                print(f"Model {m} failed (HTTP {he.code}): {err_content}", file=sys.stderr)
                if he.code in (400, 401, 403) and ('API_KEY_INVALID' in err_content or 'API key not valid' in err_content):
                    self.send_error_json(he.code, err_msg)
                    return
                # If 404 (model not found), continue to try next candidate model!
                if he.code == 404:
                    continue
            except Exception as e:
                last_error = f"Lỗi kết nối Gemini API: {str(e)}"
                print(f"Model {m} exception: {str(e)}", file=sys.stderr)
                continue

        self.send_error_json(500, last_error or 'Không thể gọi Gemini API.')

    def send_error_json(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps({
            'success': False,
            'error': message
        }, ensure_ascii=False).encode('utf-8'))

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, AIAppHandler)
    print(f"==================================================")
    print(f"🚀 AI Course Server đang chạy tại: http://localhost:{PORT}")
    print(f"🔑 Gemini Model: {GEMINI_MODEL} (maxOutputTokens: 8192 - KHÔNG GIỚI HẠN)")
    has_key = bool(GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here')
    print(f"📡 API Key Status: {'✓ Đã nạp từ .env' if has_key else '⚠️ Chưa có key trong .env (hãy thêm vào .env)'}")
    print(f"==================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã tắt server.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
