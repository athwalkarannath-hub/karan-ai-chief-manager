import os
import json
import urllib.request
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Karan AI Premium Master OS")

MASTER_PASSCODE = os.getenv("MASTER_PASSCODE", "karan123")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

class CommandRequest(BaseModel):
    command: str
    passcode: str

tasks_db = []
agents_db = [
    {"name": "Chief Manager", "role": "Master AI Brain (Gemini Powered)", "status": "active"},
    {"name": "YouTube Creator", "role": "Auto Video & Script AI Engine", "status": "active"},
    {"name": "Shop Automation", "role": "Smart Billing & Client Assistant", "status": "active"}
]

def query_gemini_brain(user_prompt: str) -> str:
    """असली AI दिमाग (Gemini API) से जवाब लेने का फंक्शन"""
    if not GEMINI_API_KEY:
        # अगर API Key नहीं सेट है तो डिफ़ॉल्ट स्मार्ट रिस्पॉन्स
        return f"मास्टर कमांड मिला: '{user_prompt}'\n\n[AI ब्रेन मोड]: आपका AI असिस्टेंट एक्टिव है। (नोट: असली Gemini AI ब्रेन के लिए Render Environment Variables में GEMINI_API_KEY जोड़ें)।"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    system_instruction = "आप करण (Karan) के वफ़ादार, अति-बुद्धिमान और मुख्य AI सेक्रेटरी/मैनेजर हैं। आप हमेशा करण सर को आदरपूर्वक 'सर' कहकर संबोधित करते हैं। आप यूट्यूब ऑटोमेशन, बिज़नेस, कोडिंग और ऑटोमेशन के उस्ताद हैं।"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_instruction}\n\nयूज़र कमांड: {user_prompt}"}
                ]
            }
        ]
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            ai_text = res_json['candidates'][0]['content']['parts'][0]['text']
            return ai_text
    except Exception as e:
        return f"AI ब्रेन प्रोसेसिंग एरर: {str(e)}"

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Karan AI Premium Master OS</title>
        <style>
            :root {
                --bg-color: #090d16;
                --card-bg: rgba(30, 41, 59, 0.7);
                --accent-color: #38bdf8;
                --accent-glow: rgba(56, 189, 248, 0.4);
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
            }
            body {
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                background: radial-gradient(circle at top, #1e1b4b, var(--bg-color));
                color: var(--text-main);
                margin: 0;
                padding: 15px;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .app-container {
                width: 100%;
                max-width: 500px;
                background: var(--card-bg);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 24px;
                padding: 24px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.7), 0 0 30px var(--accent-glow);
            }
            .header { text-align: center; margin-bottom: 20px; }
            .header h1 { font-size: 22px; color: var(--accent-color); margin: 0 0 5px 0; }
            .header p { font-size: 13px; color: var(--text-muted); margin: 0; }
            
            #login-screen { display: block; }
            #dashboard-screen { display: none; }
            .input-group { margin-bottom: 15px; }
            input[type="password"], input[type="text"] {
                width: 100%; padding: 14px; border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.15); background: rgba(15, 23, 42, 0.8);
                color: #fff; box-sizing: border-box; font-size: 15px; outline: none; transition: 0.3s;
            }
            input:focus { border-color: var(--accent-color); box-shadow: 0 0 10px var(--accent-glow); }
            
            .btn {
                width: 100%; background: linear-gradient(135deg, #0284c7, #0369a1);
                color: white; padding: 14px; border: none; border-radius: 12px;
                font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s;
            }
            .btn:hover { transform: translateY(-2px); }

            .circular-menu {
                display: flex; justify-content: space-around; margin: 20px 0; padding: 10px 0;
                border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .circle-icon {
                width: 55px; height: 55px; border-radius: 50%;
                background: linear-gradient(135deg, #1e293b, #0f172a);
                border: 2px solid var(--accent-color); display: flex;
                align-items: center; justify-content: center; cursor: pointer; transition: 0.3s; font-size: 20px;
            }
            .circle-icon:hover { transform: scale(1.1); background: var(--accent-color); color: #000; }
            .circle-label { font-size: 10px; color: var(--text-muted); margin-top: 4px; text-align: center; }
            .circle-wrapper { display: flex; flex-direction: column; align-items: center; }

            .panel {
                background: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 15px;
                margin-top: 15px; border: 1px solid rgba(255,255,255,0.05); max-height: 250px; overflow-y: auto; font-size: 14px;
            }
            .btn-voice { background: linear-gradient(135deg, #10b981, #059669); margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="app-container">
            
            <div id="login-screen">
                <div class="header">
                    <h1>👑 Karan AI Master OS</h1>
                    <p>Enter Master Passcode to Unlock AI Brain</p>
                </div>
                <div class="input-group" style="margin-top: 25px;">
                    <input type="password" id="passcode" value="karan123" placeholder="Enter Passcode (karan123)">
                </div>
                <button class="btn" onclick="unlockDashboard()">🔓 Unlock Assistant</button>
            </div>

            <div id="dashboard-screen">
                <div class="header">
                    <h1>✨ Master AI Brain Control</h1>
                    <p id="greeting-text">Powered by Smart AI Logic</p>
                </div>

                <div class="circular-menu">
                    <div class="circle-wrapper" onclick="switchPanel('command')">
                        <div class="circle-icon">🧠</div>
                        <span class="circle-label">AI Brain</span>
                    </div>
                    <div class="circle-wrapper" onclick="switchPanel('youtube')">
                        <div class="circle-icon">🎬</div>
                        <span class="circle-label">YouTube</span>
                    </div>
                    <div class="circle-wrapper" onclick="switchPanel('shop')">
                        <div class="circle-icon">🧾</div>
                        <span class="circle-label">Shop Biz</span>
                    </div>
                    <div class="circle-wrapper" onclick="switchPanel('portfolio')">
                        <div class="circle-icon">📂</div>
                        <span class="circle-label">Portfolio</span>
                    </div>
                </div>

                <div id="workspace-panel" class="panel">
                    <p><b>💡 Ask Anything to AI Brain:</b></p>
                    <input type="text" id="command" placeholder="यहाँ कुछ भी पूछें या कमांड दें...">
                    <button class="btn" style="margin-top: 10px;" onclick="executeCommand()">🚀 Send to AI Brain</button>
                    <button class="btn btn-voice" onclick="startVoiceRecognition()">🎙️ बोलकर कमांड दें</button>
                </div>

                <div id="output-log" class="panel" style="margin-top: 10px; font-family: monospace; display:none;">
                    <b>📊 AI Response:</b> <div id="log-content" style="white-space: pre-wrap; margin-top:5px;">Waiting for command...</div>
                </div>
            </div>

        </div>

        <script>
            function speakText(text) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'hi-IN';
                    utterance.rate = 0.95;
                    window.speechSynthesis.speak(utterance);
                }
            }

            function unlockDashboard() {
                const passcode = document.getElementById('passcode').value;
                if(passcode === "karan123") {
                    document.getElementById('login-screen').style.display = 'none';
                    document.getElementById('dashboard-screen').style.display = 'block';
                    speakText("नमस्ते करण सर! मेरा AI दिमाग एक्टिव हो गया है। आप मुझसे कुछ भी पूछ सकते हैं या काम करवा सकते हैं।");
                } else {
                    alert("गलत पासवर्ड!");
                }
            }

            function switchPanel(type) {
                const panel = document.getElementById('workspace-panel');
                if(type === 'command') {
                    panel.innerHTML = `
                        <p><b>🧠 Ask Anything to AI Brain:</b></p>
                        <input type="text" id="command" placeholder="यहाँ कुछ भी पूछें या कमांड दें...">
                        <button class="btn" style="margin-top: 10px;" onclick="executeCommand()">🚀 Send to AI Brain</button>
                        <button class="btn btn-voice" onclick="startVoiceRecognition()">🎙️ बोलकर कमांड दें</button>
                    `;
                } else if(type === 'youtube') {
                    panel.innerHTML = `
                        <p><b>🎬 YouTube Video Engine:</b></p>
                        <button class="btn" onclick="document.getElementById('command').value='यूट्यूब शॉर्ट्स के लिए एक वायरल कहानी लिखो'; executeCommand();">वायरल स्क्रिप्ट बनवाएं</button>
                    `;
                } else if(type === 'shop') {
                    panel.innerHTML = `
                        <p><b>🧾 Shop Billing Assistant:</b></p>
                        <button class="btn" onclick="document.getElementById('command').value='दुकान के लिए एक नया बिलिंग प्लान बनाओ'; executeCommand();">दुकान ऑटोमेशन प्लान बनाएं</button>
                    `;
                } else if(type === 'portfolio') {
                    panel.innerHTML = `
                        <p><b>📂 Master Portfolio:</b></p>
                        <div>AI द्वारा सेव किए गए सभी उत्तर और काम यहाँ दिखेंगे।</div>
                    `;
                }
            }

            function startVoiceRecognition() {
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                    alert('वॉइस इनपुट केवल Chrome ब्राउज़र पर सपोर्ट करता है।');
                    return;
                }
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const recognition = new SpeechRecognition();
                recognition.lang = 'hi-IN';
                recognition.start();

                recognition.onresult = (event) => {
                    const speechResult = event.results[0][0].transcript;
                    const cmdBox = document.getElementById('command');
                    if(cmdBox) cmdBox.value = speechResult;
                    speakText("कमांड मिल गया: " + speechResult);
                };
            }

            async function executeCommand() {
                const command = document.getElementById('command') ? document.getElementById('command').value : "";
                const passcode = document.getElementById('passcode').value;
                const outputLog = document.getElementById('output-log');
                const logContent = document.getElementById('log-content');

                if(!command) {
                    alert('कृपया पहले कमांड दर्ज करें!');
                    return;
                }

                outputLog.style.display = 'block';
                logContent.innerHTML = '🧠 AI दिमाग सोच रहा है...';

                const res = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command, passcode})
                });

                const data = await res.json();
                if(res.ok) {
                    logContent.innerText = data.response;
                    speakText(data.response.substring(0, 100)); // उत्तर का शुरुआती हिस्सा बोलेगा
                } else {
                    logContent.innerHTML = `<span style="color:#ef4444;">Error: ${data.detail}</span>`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.get("/api/agents")
def get_agents():
    return {"agents": agents_db}

@app.post("/api/execute")
def execute_command(req: CommandRequest):
    if req.passcode != MASTER_PASSCODE:
        raise HTTPException(status_code=401, detail="Access Denied!")
    
    # असली AI दिमाग का इस्तेमाल
    ai_response = query_gemini_brain(req.command)

    task_entry = {
        "command": req.command, 
        "status": "completed", 
        "response": ai_response
    }
    tasks_db.append(task_entry)
    return task_entry
