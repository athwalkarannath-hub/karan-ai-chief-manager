import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="Karan AI Chief Manager")

# मास्टर पासवर्ड सिक्योरिटी (डिफ़ॉल्ट: karan123)
MASTER_PASSCODE = os.getenv("MASTER_PASSCODE", "karan123")

class CommandRequest(BaseModel):
    command: str
    passcode: str

# डाटाबेस / मेमोरी (In-memory Storage)
tasks_db = []
agents_db = [
    {"name": "Chief Manager", "role": "Owner-controlled Master Agent", "status": "active"},
    {"name": "YouTube Creator", "role": "Auto Video Script & Upload Manager", "status": "active"},
    {"name": "Shop Automation", "role": "Billing & Client Service Tool", "status": "active"}
]

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Karan AI Master Operating System</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
            .container { max-width: 800px; margin: 0 auto; background: #1e293b; padding: 25px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }
            h1 { color: #38bdf8; text-align: center; font-size: 24px; margin-bottom: 20px; }
            .card { background: #334155; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #38bdf8; }
            input[type="text"], input[type="password"] { width: 100%; padding: 12px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #fff; box-sizing: border-box; }
            button { width: 100%; background: #0284c7; color: white; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; font-size: 16px; margin-top: 10px; }
            button:hover { background: #0369a1; }
            .status { font-weight: bold; color: #4ade80; }
            .task-box { background: #0f172a; padding: 10px; border-radius: 6px; margin-top: 10px; white-space: pre-wrap; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>👑 Karan AI Master Chief Control</h1>
            
            <div class="card">
                <h3>🔐 Security Lock & Command Center</h3>
                <input type="password" id="passcode" placeholder="Enter Master Passcode (Default: karan123)">
                <input type="text" id="command" placeholder="Type your master command or tool creation request...">
                <button onclick="submitCommand()">Execute Command</button>
            </div>

            <div class="card">
                <h3>🤖 Active Agents</h3>
                <div id="agents-list">Loading active sub-agents...</div>
            </div>

            <div class="card">
                <h3>📊 Execution Logs & Task Output</h3>
                <div id="output-log">No tasks executed yet.</div>
            </div>
        </div>

        <script>
            async function loadAgents() {
                const res = await fetch('/api/agents');
                const data = await res.json();
                let html = '<ul>';
                data.agents.forEach(a => {
                    html += `<li><b>${a.name}</b> (${a.role}) - <span class="status">${a.status}</span></li>`;
                });
                html += '</ul>';
                document.getElementById('agents-list').innerHTML = html;
            }

            async function submitCommand() {
                const command = document.getElementById('command').value;
                const passcode = document.getElementById('passcode').value;
                const outputLog = document.getElementById('output-log');

                if(!command || !passcode) {
                    alert('Please enter both passcode and command!');
                    return;
                }

                outputLog.innerHTML = 'Processing command...';

                const res = await fetch('/api/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({command, passcode})
                });

                const data = await res.json();
                if(res.ok) {
                    outputLog.innerHTML = `<div class="task-box"><b>Command:</b> ${data.command}\n\n<b>Status:</b> ${data.status}\n\n<b>Response / Plan:</b>\n${data.response}</div>`;
                } else {
                    outputLog.innerHTML = `<span style="color: #ef4444;">Error: ${data.detail}</span>`;
                }
            }

            loadAgents();
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
        raise HTTPException(status_code=401, detail="Access Denied! Incorrect Master Passcode.")
    
    cmd = req.command.lower()
    
    # स्मार्ट रिस्पॉन्स और टूल्स लॉजिक
    if "youtube" in cmd or "वीडियो" in cmd:
        response = "YouTube Automation Agent Activated:\n1. Topic research initialized.\n2. Viral script generated.\n3. Ready for automated render and upload pipeline."
    elif "shop" in cmd or "दूकान" in cmd or "bill" in cmd:
        response = "Micro-Shop Billing & Automation Tool Activated:\n1. Generating automated customer receipt template.\n2. Syncing local inventory status."
    else:
        response = f"Master Request Processed:\nCommand understood: '{req.command}'\nPlan: Analyzing request, breaking down tasks, and delegating to sub-agents safely."

    task_entry = {"command": req.command, "status": "completed", "response": response}
    tasks_db.append(task_entry)
    
    return task_entry
