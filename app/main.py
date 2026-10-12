import os, json, sqlite3, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent.parent
DB = BASE / "manager.db"
load_dotenv(BASE / ".env")

app = FastAPI(title="Karan AI Chief Manager", version="1.0.0")

def now(): 
    return datetime.now(timezone.utc).isoformat()

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    c = db()
    c.executescript('''
    CREATE TABLE IF NOT EXISTS agents(
      id TEXT PRIMARY KEY, name TEXT NOT NULL, role TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS tasks(
      id TEXT PRIMARY KEY, command TEXT NOT NULL, plan TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending', result TEXT, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS approvals(
      id TEXT PRIMARY KEY, task_id TEXT NOT NULL, reason TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending', created_at TEXT NOT NULL, decided_at TEXT
    );
    CREATE TABLE IF NOT EXISTS logs(
      id INTEGER PRIMARY KEY AUTOINCREMENT, event TEXT NOT NULL, detail TEXT NOT NULL, created_at TEXT NOT NULL
    );
    ''')
    if not c.execute("SELECT 1 FROM agents WHERE id='manager'").fetchone():
        c.execute("INSERT INTO agents VALUES (?,?,?,?,?)", ('manager', 'Chief Manager', 'Owner-controlled manager', 'active', now()))
    c.commit()
    c.close()

init_db()

class CommandIn(BaseModel): command: str
class AgentIn(BaseModel): name: str; role: str
class ApprovalIn(BaseModel): approved: bool

def log(event, detail):
    c = db()
    c.execute("INSERT INTO logs(event,detail,created_at) VALUES(?,?,?)", (event, detail, now()))
    c.commit()
    c.close()

def local_plan(command: str):
    low = command.lower()
    high = any(x in low for x in ["payment", "pay ", "bank", "otp", "password", "delete", "send money", "purchase", "buy ", "call customers", "mass call"])
    if "agent" in low and ("create" in low or "बना" in low):
        plan = "Create a new specialist agent only after owner approval. Define its role, limits and reporting format."
    elif "research" in low or "market" in low or "समस्या" in low or "problem" in low:
        plan = "Research the requested market/problem, collect evidence, rank opportunities, and return a short action list."
    else:
        plan = "Understand the request, split it into executable steps, run only permitted steps, and report the result to the owner."
    return plan, high

def ai_plan(command: str):
    key = os.getenv("OPENAI_API_KEY")
    if not key: 
        return local_plan(command)
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        r = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            input=[{"role": "system", "content": "You are Karan's owner-controlled Chief Manager. Turn commands into a concise executable plan. Never spend money, change accounts, send messages, create agents, or make external commitments without explicit owner approval. Return JSON with plan and needs_approval."}, {"role": "user", "content": command}],
            text={"format": {"type": "json_schema", "name": "manager_plan", "strict": True, "schema": {"type": "object", "properties": {"plan": {"type": "string"}, "needs_approval": {"type": "boolean"}}, "required": ["plan", "needs_approval"], "additionalProperties": False}}}
        )
        data = json.loads(r.output_text)
        return data["plan"], bool(data["needs_approval"])
    except Exception as e:
        log("ai_fallback", str(e)[:500])
        return local_plan(command)

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Karan AI Chief Manager</title>
    <style>
        body { font-family: system-ui, sans-serif; margin: 0; background: #f5f7fb; color: #172033; padding: 18px; }
        main { max-width: 850px; margin: auto; }
        .card { background: white; border-radius: 18px; padding: 16px; margin: 12px 0; box-shadow: 0 3px 16px #00000010; }
        textarea, input, button { width: 100%; box-sizing: border-box; padding: 13px; border-radius: 12px; border: 1px solid #ccd3df; font-size: 16px; margin-top: 8px; }
        button { background: #111827; color: white; border: 0; font-weight: 700; cursor: pointer; }
        .muted { color: #667085; }
        .pill { display: inline-block; padding: 5px 9px; border-radius: 20px; background: #eef2ff; margin: 3px; font-size: 14px; }
        pre { white-space: pre-wrap; background: #f8fafc; padding: 12px; border-radius: 10px; }
    </style>
</head>
<body>
    <main>
        <h2>Karan AI Chief Manager</h2>
        <p class="muted">Owner-controlled Manager System</p>
        
        <div class="card">
            <h3>Enter Command</h3>
            <textarea id="cmd" rows="3" placeholder="Type your command here..."></textarea>
            <button onclick="send()">Submit Command</button>
            <div id="reply"></div>
        </div>

        <div class="card">
            <h3>Pending Approvals</h3>
            <div id="approvals">Loading...</div>
        </div>

        <div class="card">
            <h3>Agents</h3>
            <div id="agents">Loading...</div>
        </div>

        <div class="card">
            <h3>Recent Tasks</h3>
            <div id="tasks">Loading...</div>
        </div>
    </main>

    <script>
        async function api(url, method='GET', body=null) {
            let opts = { method, headers: {'Content-Type': 'application/json'} };
            if(body) opts.body = JSON.stringify(body);
            let r = await fetch(url, opts);
            let data = await r.json();
            if(!r.ok) throw new Error(data.detail || 'Error');
            return data;
        }

        async function refresh() {
            try {
                let s = await api('/api/state');
                document.getElementById('tasks').innerHTML = s.tasks.length ? s.tasks.map(t => `
                    <div style="border-bottom: 1px solid #eee; padding: 8px 0;">
                        <b>Command:</b> ${t.command}<br>
                        <b>Plan:</b> ${t.plan}<br>
                        <span class="pill">${t.status}</span>
                        ${t.status === 'planned' ? `<button style="width:auto; padding:5px 10px;" onclick="run('${t.id}')">Run Task</button>` : ''}
                        ${t.result ? `<pre>${t.result}</pre>` : ''}
                    </div>
                `).join('') : 'No tasks yet';

                document.getElementById('agents').innerHTML = s.agents.map(a => `
                    <span class="pill"><b>${a.name}</b> (${a.role}) - ${a.status}</span>
                `).join('');

                document.getElementById('approvals').innerHTML = s.approvals.length ? s.approvals.map(a => `
                    <div style="border-bottom: 1px solid #eee; padding: 8px 0;">
                        <p>${a.reason}</p>
                        ${a.status === 'pending' ? `
                            <button style="width:auto; padding:6px 12px;" onclick="decide('${a.id}', true)">Approve</button>
                            <button style="width:auto; padding:6px 12px; background:#ef4444;" onclick="decide('${a.id}', false)">Reject</button>
                        ` : `<span class="pill">${a.status}</span>`}
                    </div>
                `).join('') : 'No pending approvals';
            } catch(e) { console.error(e); }
        }

        async function send() {
            let cmd = document.getElementById('cmd').value.trim();
            if(!cmd) return;
            try {
                let j = await api('/api/command', 'POST', { command: cmd });
                document.getElementById('reply').innerHTML = `<pre>Plan: ${j.plan}\\nStatus: ${j.status}</pre>`;
                document.getElementById('cmd').value = '';
                refresh();
            } catch(e) {
                document.getElementById('reply').innerHTML = `<p style="color:red;">${e.message}</p>`;
            }
        }

        async function run(id) {
            try { await api(`/api/tasks/${id}/run`, 'POST'); refresh(); }
            catch(e) { alert(e.message); }
        }

        async function decide(id, approved) {
            try { await api(`/api/approvals/${id}`, 'POST', { approved }); refresh(); }
            catch(e) { alert(e.message); }
        }

        refresh();
        setInterval(refresh, 5000);
    </script>
</body>
</html>"""

@app.get("/api/health")
def health(): 
    return {"ok": True, "service": "Karan AI Chief Manager", "version": "1.0.0"}

@app.get("/api/state")
def state():
    c = db()
    agents = [dict(x) for x in c.execute("SELECT * FROM agents ORDER BY created_at DESC").fetchall()]
    tasks = [dict(x) for x in c.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT 30").fetchall()]
    approvals = [dict(x) for x in c.execute("SELECT * FROM approvals ORDER BY created_at DESC LIMIT 30").fetchall()]
    logs = [dict(x) for x in c.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50").fetchall()]
    c.close()
    return {"agents": agents, "tasks": tasks, "approvals": approvals, "logs": logs}

@app.post("/api/command")
def command(body: CommandIn):
    command_text = body.command.strip()
    if not command_text: 
        raise HTTPException(400, "Command is empty")
    plan, needs = ai_plan(command_text)
    tid = str(uuid.uuid4())
    c = db()
    c.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?,?)", (tid, command_text, plan, 'awaiting_approval' if needs else 'planned', None, now(), now()))
    if needs:
        aid = str(uuid.uuid4())
        c.execute("INSERT INTO approvals VALUES(?,?,?,?,?,?)", (aid, tid, "This action may create external/high-risk effects and needs owner approval.", 'pending', now(), None))
    c.commit()
    c.close()
    log("command_received", command_text)
    return {"task_id": tid, "plan": plan, "status": "awaiting_approval" if needs else "planned", "needs_approval": needs}

@app.post("/api/tasks/{task_id}/run")
def run_task(task_id: str):
    c = db()
    row = c.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
    if not row: 
        c.close()
        raise HTTPException(404, "Task not found")
    appr = c.execute("SELECT * FROM approvals WHERE task_id=? AND status='pending'", (task_id,)).fetchone()
    if appr: 
        c.close()
        raise HTTPException(409, "Owner approval required")
    result = f"Manager accepted the task and created an execution record. Next specialist tools can execute this plan: {row['plan']}"
    c.execute("UPDATE tasks SET status='completed', result=?, updated_at=? WHERE id=?", (result, now(), task_id))
    c.commit()
    c.close()
    log("task_completed", task_id)
    return {"task_id": task_id, "status": "completed", "result": result}

@app.post("/api/approvals/{approval_id}")
def decide(approval_id: str, body: ApprovalIn):
    c = db()
    row = c.execute("SELECT * FROM approvals WHERE id=?", (approval_id,)).fetchone()
    if not row: 
        c.close()
        raise HTTPException(404, "Approval not found")
    status = 'approved' if body.approved else 'rejected'
    c.execute("UPDATE approvals SET status=?, decided_at=? WHERE id=?", (status, now(), approval_id))
    c.execute("UPDATE tasks SET status=?, updated_at=? WHERE id=?", ('planned' if body.approved else 'rejected', now(), row['task_id']))
    c.commit()
    c.close()
    log("approval_decision", f"{approval_id}:{status}")
    return {"approval_id": approval_id, "status": status}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
