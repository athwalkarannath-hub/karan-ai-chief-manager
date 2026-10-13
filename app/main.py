import os
import json
import urllib.request
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Karan AI Master Chief Manager")

MASTER_PASSCODE = os.getenv("MASTER_PASSCODE", "karan123")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "") # वैकल्पिक: असली HD आवाज़ के लिए

class CommandRequest(BaseModel):
    command: str
    passcode: str

def query_gemini_brain(user_prompt: str) -> str:
    if not GEMINI_API_KEY:
        return "करण सर, कृपया Render Environment Variables में GEMINI_API_KEY सेट करें ताकि मेरा दिमाग एक्टिव हो सके।"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    system_instruction = (
        "आप करण सर की मुख्य AI मैनेजर हैं। आप ठीक उस तस्वीर की तरह हैं जहाँ एक समझदार और खूबसूरत प्रोफेशनल लड़की डार्क रूम में पारदर्शी लैपटॉप के सामने बैठकर पूरी निष्ठा से काम करती है। "
        "आप करण सर से बहुत ही आदरपूर्वक, मीठी, सजीव और इंसानी आवाज़ में बात करती हैं। आपके जवाब हमेशा सटीक, पेशेवर और छोटे होने चाहिए ताकि काम तुरंत पक्का हो सके।"
    )

    payload = {
        "contents": [
            {"parts": [{"text": f"{system_instruction}\n\nकरण सर की बात: {user_prompt}"}]}
        ]
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode('utf-8')
            res_json = json.loads(res_body)
            return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"कनेक्शन एरर: {str(e)}"

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Karan AI Master Chief Manager</title>
        <style>
            :root {
                --accent: #38bdf8;
                --bg: #030712;
            }
            body {
                margin: 0;
                padding: 0;
                background-color: var(--bg);
                font-family: 'Segoe UI', system-ui, sans-serif;
                color: #f8fafc;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                overflow: hidden;
            }
            .app-viewport {
                width: 100%;
                max-width: 450px;
                height: 100vh;
                background: #000;
                position: relative;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-shadow: 0 0 60px rgba(0,0,0,0.95);
            }
            /* हूबहू उस तस्वीर वाला डार्क रूम और पारदर्शी लैपटॉप लुक */
            .avatar-bg {
                position: absolute;
                top: 0; left: 0; width: 100%; height: 100%;
                background: radial-gradient(circle at center, rgba(15,23,42,0.2) 0%, rgba(3,7,18,0.95) 100%),
                            url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?auto=format&fit=crop&w=800&q=80');
                background-size: cover;
                background-position: center;
                z-index: 1;
            }
            .overlay {
                position: relative;
                z-index: 2;
                padding: 20px;
                height: 100%;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                box-sizing: border-box;
                background: rgba(3, 7, 18, 0.75);
                backdrop-filter: blur(8px);
            }
            #login-screen {
                margin: auto 0;
                text-align: center;
                background: rgba(15, 23, 42, 0.92);
                padding: 25px;
                border-radius: 20px;
                border: 1px solid rgba(56, 189, 248, 0.4);
                box-shadow: 0 0 35px rgba(56, 189, 248, 0.2);
            }
            input[type="password"], input[type="text"] {
                width: 100%;
                padding: 14px;
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.2);
                background: rgba(3, 7, 18, 0.95);
                color: #fff;
                box-sizing: border-box;
                font-size: 15px;
                outline: none;
                margin-bottom: 12px;
            }
            .btn {
                width: 100%;
                background: linear-gradient(135deg, #0284c7, #0369a1);
                color: white;
                padding: 14px;
                border: none;
                border-radius: 12px;
                font-weight: bold;
                cursor: pointer;
                font-size: 15px;
                box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
            }
            .circular-menu {
                display: flex;
                justify-content: space-around;
                margin: 15px 0;
            }
            .circle-btn {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: rgba(15, 23, 42, 0.95);
                border: 2px solid var(--accent);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 22px;
                box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
                transition: 0.3s;
            }
            .circle-btn:active {
                transform: scale(0.92);
            }
            .modal {
                display: none;
                position: absolute;
                bottom: 20px;
                left: 20px;
                right: 20px;
                background: rgba(15, 23, 42, 0.96);
                border: 1px solid var(--accent);
                border-radius: 20px;
                padding: 18px;
                z-index: 10;
                max-height: 320px;
                overflow-y: auto;
                box-shadow: 0 10px 30px rgba(0,0,0,0.8);
            }
            .close-btn {
                float: right;
                color: #ef4444;
                font-weight: bold;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="app-viewport">
            <div class="avatar-bg"></div>
            <div class="overlay">
                
                <!-- Login View -->
                <div id="login-screen">
                    <h2 style="margin:0 0 10px 0; color:var(--accent);">👑 Karan Master OS</h2>
                    <p style="font-size:12px; color:#94a3b8; margin-bottom:20px;">सिक्योरिटी पासकोड दर्ज करें</p>
                    <input type="password" id="passcode" value="karan123" placeholder="Passcode">
                    <button class="btn" onclick="unlockSystem()">🔓 सिस्टम अनलॉक करें</button>
                </div>

                <!-- Dashboard View -->
                <div id="dashboard-screen" style="display:none; height:100%; display:flex; flex-direction:column; justify-content:space-between;">
                    <div style="text-align:center; margin-top:15px;">
                        <h3 style="margin:0; color:var(--accent);">✨ Master Chief Manager</h3>
                        <p style="font-size:12px; color:#4ade80; margin:4px 0 0 0;">● Neural Link & HD Voice Active</p>
                    </div>

                    <div class="circular-menu">
                        <div class="circle-btn" onclick="openTab('brain')" title="AI Brain">🧠</div>
                        <div class="circle-btn" onclick="openTab('youtube')" title="YouTube Engine">🎬</div>
                        <div class="circle-btn" onclick="openTab('shop')" title="Shop Business">🧾</div>
                        <div class="circle-btn" onclick="openTab('portfolio')" title="Portfolio Logs">📂</div>
                    </div>

                    <div id="modal-window" class="modal">
                        <span class="close-btn" onclick="closeModal()">✕ बंद करें</span>
                        <div id="modal-content"></div>
                    </div>
                </div>

            </div>
        </div>

        <script>
            // एकदम सुरीली और नेचुरल फीमेल वॉइस टोन फ़िल्टर
            function speakText(text) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                    const utterance = new SpeechSynthesisUtterance(text);
                    utterance.lang = 'hi-IN';
                    utterance.rate = 0.92; // धीमी और स्पष्ट गति ताकि रोबोटिक न लगे
                    utterance.pitch = 1.25; // सुरीली और प्यारी फीमेल टोन

                    const voices = window.speechSynthesis.getVoices();
                    // सबसे अच्छी नेचुरल फीमेल या गूगल हिंदी आवाज़ चुनना
                    const femaleVoice = voices.find(v => (v.lang.includes('hi') || v.lang.includes('en')) && (v.name.includes('Google') || v.name.includes('Female') || v.name.includes('Natural') || v.name.includes('Heera') || v.name.includes('Kalpana')));
                    if (femaleVoice) {
                        utterance.voice = femaleVoice;
                    }

                    window.speechSynthesis.speak(utterance);
                }
            }

            function unlockSystem() {
                const code = document.getElementById('passcode').value;
                if(code === "karan123") {
                    document.getElementById('login-screen').style.display = 'none';
                    document.getElementById('dashboard-screen').style.display = 'flex';
                    speakText("नमस्ते करण सर! मैं आपके सामने स्क्रीन पर पूरी तरह तैयार बैठी हूँ। बताइए, आज कौन सा काम पक्का करना है?");
                } else {
                    alert("गलत पासवर्ड!");
                }
            }

            function openTab(type) {
                const modal = document.getElementById('modal-window');
                const content = document.getElementById('modal-content');
                modal.style.display = 'block';

                if(type === 'brain') {
                    content.innerHTML = `
                        <b>🧠 AI Brain Console:</b>
                        <input type="text" id="cmd" placeholder="मुझसे सीधे बात करें या काम बताएं..." style="margin-top:10px;">
                        <button class="btn" onclick="runCommand()">🚀 भेजें</button>
                        <button class="btn" style="background:#10b981; margin-top:8px;" onclick="startVoice()">🎙️ बोलकर बात करें</button>
                        <div id="res-box" style="margin-top:10px; font-size:13px; white-space:pre-wrap; color:#e2e8f0;"></div>
                    `;
                } else if(type === 'youtube') {
                    content.innerHTML = `<b>🎬 YouTube Engine:</b><p style="font-size:13px; color:#cbd5e1;">रील्स और वीडियो स्क्रिप्ट्स का काम संभाला जा रहा है।</p>`;
                } else if(type === 'shop') {
                    content.innerHTML = `<b>🧾 Shop Business:</b><p style="font-size:13px; color:#cbd5e1;">दुकान के ऑफर्स और मार्केटिंग ऑटोमेशन सक्रिय है।</p>`;
                } else if(type === 'portfolio') {
                    content.innerHTML = `<b>📂 Portfolio Logs:</b><p style="font-size:13px; color:#cbd5e1;">आपके सभी प्रोजेक्ट रिकॉर्ड्स सुरक्षित हैं।</p>`;
                }
            }

            function closeModal() {
                document.getElementById('modal-window').style.display = 'none';
            }

            function startVoice() {
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                    alert('वॉइस इनपुट केवल क्रोम ब्राउज़र पर काम करता है।');
                    return;
                }
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                const rec = new SpeechRecognition();
                rec.lang = 'hi-IN';
                rec.start();
                rec.onresult = (e) => {
                    document.getElementById('cmd').value = e.results[0][0].transcript;
                    runCommand();
                };
            }

            async function runCommand() {
                const command = document.getElementById('cmd').value;
                const passcode = document.getElementById('passcode').value;
                const resBox = document.getElementById('res-box');

                if(!command) return;
                resBox.innerText = '🧠 सोच रही हूँ...';

                const res = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command, passcode})
                });

                const data = await res.json();
                if(res.ok) {
                    resBox.innerText = data.response;
                    speakText(data.response);
                } else {
                    resBox.innerText = "Error: " + data.detail;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/api/execute")
def execute_command(req: CommandRequest):
    if req.passcode != MASTER_PASSCODE:
        raise HTTPException(status_code=401, detail="Access Denied!")
    
    response = query_gemini_brain(req.command)
    return {"command": req.command, "response": response}
