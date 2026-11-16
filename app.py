from flask import Flask, request, redirect, render_template_string, send_from_directory, session
from werkzeug.utils import secure_filename
from functools import wraps
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ambadijayesh")

FOLDERS = {
    "photos": "photos",
    "videos": "uploads",
    "wallpapers": "wallpapers",
    "clips": "clips"
}

ALLOWED = {
    "photos": (".jpg", ".jpeg", ".png", ".webp", ".gif"),
    "videos": (".mp4", ".webm", ".mov", ".mkv"),
    "wallpapers": (".jpg", ".jpeg", ".png", ".webp"),
    "clips": (".mp4", ".webm", ".mov", ".mkv")
}

for folder in FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

DATA_FILE = "pluto_data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"likes": {}, "comments": {}, "notifications": [], "messages": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PLUTO GAMING</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
*{box-sizing:border-box}
body{margin:0;background:#050505;color:white;font-family:Arial;overflow-x:hidden}
header{text-align:center;padding:35px 15px;background:linear-gradient(135deg,#080808,#250000,#080808);border-bottom:2px solid red;box-shadow:0 0 25px #ff101055}
header h1{font-size:36px;color:#ff2020;letter-spacing:5px;text-shadow:0 0 15px red;animation:glow 2s infinite alternate;margin:0}
header p{color:#ddd;letter-spacing:3px;font-size:12px}
@keyframes glow{to{text-shadow:0 0 30px red,0 0 45px red}}
.container{padding:18px;max-width:850px;margin:auto}
.card{background:linear-gradient(145deg,#171717,#090909);border:1px solid #5b0808;padding:20px;margin:18px 0;border-radius:12px;box-shadow:0 0 15px #ff000022;animation:fade 1s}
@keyframes fade{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
h2{color:#ff3030;text-transform:uppercase}
button{background:linear-gradient(90deg,#8b0000,#ff1717);color:white;border:1px solid #ff5555;padding:12px 18px;border-radius:7px;font-weight:bold;cursor:pointer;margin:5px}
input,textarea,select{width:100%;max-width:100%;margin:10px 0;padding:11px;background:#171717;color:white;border:1px solid #aa1515;border-radius:6px}
textarea{min-height:75px}
video,img.media{width:100%;max-height:430px;object-fit:contain;border-radius:10px;border:1px solid #ff2525}
a{color:#ff5555;text-decoration:none}
.section-title{border-left:4px solid red;padding-left:12px;margin-top:30px}
.tag{display:inline-block;color:#ff3030;border:1px solid #ff3030;padding:7px 12px;margin:5px;border-radius:20px;font-size:12px}
footer{text-align:center;padding:25px;color:#777;border-top:1px solid #5b0808}
.notice{border-left:3px solid red;padding:10px;background:#200707;margin:10px 0}
.small{color:#aaa;font-size:12px}
.search{border:1px solid red;font-size:16px}
.particle{position:fixed;bottom:-10px;width:4px;height:4px;background:red;border-radius:50%;box-shadow:0 0 10px red;pointer-events:none;animation:rise 7s linear infinite;z-index:-1}
@keyframes rise{to{transform:translateY(-110vh);opacity:0}}
.hidden{display:none}
</style>
</head>
<body>

<header>
<h1>PLUTO GAMING</h1>
<p>UNLEASH YOUR GAMING POWER</p>
<div>
<span class="tag">BGMI GAMING</span>
<span class="tag">VIDEOS</span>
<span class="tag">HIGHLIGHTS</span>
</div>
</header>

<div class="container">

<div class="card">
<h2>Welcome To Pluto Gaming</h2>
<p>Enter the battleground. Experience gaming highlights and latest updates.</p>
</div>

<input class="search" id="search" placeholder="🔍 Search photos, videos, clips...">

{% if notifications %}
<div class="card">
<h2>🔔 Notifications</h2>
{% for n in notifications %}
<div class="notice">{{ n.text }}<div class="small">{{ n.date }}</div></div>
{% endfor %}
</div>
{% endif %}

{% if admin %}
<div class="card">
<h2>Admin Dashboard</h2>
<form action="/upload" method="POST" enctype="multipart/form-data">
<select name="kind" required>
<option value="videos">Upload Video</option>
<option value="photos">Upload Photo</option>
<option value="wallpapers">Upload Wallpaper</option>
<option value="clips">Upload Gaming Clip</option>
</select>
<input type="file" name="file" required>
<button type="submit">UPLOAD</button>
</form>

<h2>Post Notification</h2>
<form action="/notify" method="POST">
<input name="text" placeholder="Notification message" required>
<button>POST NOTIFICATION</button>
</form>

<h2>Admin Messages</h2>
{% for m in messages %}
<div class="notice">{{ m.text }}<div class="small">{{ m.date }}</div></div>
{% else %}
<p>No messages yet.</p>
{% endfor %}
<a href="/logout">Logout</a>
</div>
{% else %}
<div class="card">
<h2>Admin Login</h2>
<form action="/login" method="POST">
<input type="password" name="password" placeholder="Admin password" required>
<button>LOGIN</button>
</form>
</div>
{% endif %}

{% for section in sections %}
<h2 class="section-title">{{ section.title }}</h2>
{% for item in section["items"] %}
<div class="card media-card" data-search="{{ item.filename|lower }} {{ section.title|lower }}">
{% if item.kind in ["videos","clips"] %}
<video controls preload="metadata">
<source src="/media/{{ item.kind }}/{{ item.filename }}">
</video>
{% else %}
<img class="media" src="/media/{{ item.kind }}/{{ item.filename }}" loading="lazy">
{% endif %}
<p>{{ item.filename }}</p>
<form action="/like" method="POST">
<input type="hidden" name="key" value="{{ item.key }}">
<button>❤️ LIKE ({{ item.likes }})</button>
</form>
<h3>Comments</h3>
{% for c in item.comments %}
<div class="notice">{{ c }}</div>
{% endfor %}
<form action="/comment" method="POST">
<input type="hidden" name="key" value="{{ item.key }}">
<input name="comment" placeholder="Write a comment..." maxlength="300" required>
<button>COMMENT</button>
</form>
</div>
{% else %}
<div class="card">No {{ section.title|lower }} uploaded yet.</div>
{% endfor %}
{% endfor %}

<div class="card">
<h2>Contact Admin</h2>
<form action="/contact" method="POST">
<input name="name" placeholder="Your name" maxlength="50" required>
<textarea name="message" placeholder="Your message" maxlength="1000" required></textarea>
<button>SEND MESSAGE</button>
</form>
</div>

<div class="card">
<h2>Instagram</h2>
<a href="https://www.instagram.com/pluto_ser_her/" target="_blank">
<button>VISIT INSTAGRAM</button>
</a>
</div>

</div>
<footer>PLUTO GAMING © 2026</footer>

<script>
const search = document.getElementById("search");
search.addEventListener("input", () => {
 const q = search.value.toLowerCase();
 document.querySelectorAll(".media-card").forEach(card => {
  card.classList.toggle("hidden", !card.dataset.search.includes(q));
 });
});

for(let i=0;i<25;i++){
 const p=document.createElement("div");
 p.className="particle";
 p.style.left=Math.random()*100+"%";
 p.style.animationDelay=Math.random()*7+"s";
 p.style.animationDuration=(5+Math.random()*6)+"s";
 document.body.appendChild(p);
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    data = load_data()
    sections = []

    titles = {
        "photos": "Photo Gallery",
        "wallpapers": "Gaming Wallpapers",
        "videos": "Video Gallery",
        "clips": "Gaming Clips"
    }

    for kind, title in titles.items():
        items = []
        folder = FOLDERS[kind]
        for filename in sorted(os.listdir(folder), reverse=True):
            path = os.path.join(folder, filename)
            if not os.path.isfile(path):
                continue
            key = kind + ":" + filename
            items.append({
                "kind": kind,
                "filename": filename,
                "key": key,
                "likes": data["likes"].get(key, 0),
                "comments": data["comments"].get(key, [])
            })
        sections.append({"title": title, "items": items})

    return render_template_string(
        HTML,
        sections=sections,
        admin=session.get("admin", False),
        notifications=data["notifications"],
        messages=data["messages"] if session.get("admin") else []
    )

@app.route("/login", methods=["POST"])
def login():
    if request.form.get("password") == ADMIN_PASSWORD:
        session["admin"] = True
        return redirect("/")
    return "Wrong password", 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/upload", methods=["POST"])
@admin_required
def upload():
    kind = request.form.get("kind")
    file = request.files.get("file")

    if kind not in FOLDERS or not file or not file.filename:
        return "Invalid upload", 400

    filename = secure_filename(file.filename)
    if not filename or not filename.lower().endswith(ALLOWED[kind]):
        return "Unsupported file type", 400

    filename = uuid.uuid4().hex[:8] + "_" + filename
    file.save(os.path.join(FOLDERS[kind], filename))
    return redirect("/")

@app.route("/media/<kind>/<path:filename>")
def media(kind, filename):
    if kind not in FOLDERS:
        return "Not found", 404
    return send_from_directory(FOLDERS[kind], filename)

@app.route("/like", methods=["POST"])
def like():
    key = request.form.get("key", "")
    if ":" not in key:
        return "Invalid item", 400
    kind, filename = key.split(":", 1)
    if kind not in FOLDERS or not os.path.isfile(os.path.join(FOLDERS[kind], filename)):
        return "Not found", 404
    data = load_data()
    data["likes"][key] = data["likes"].get(key, 0) + 1
    save_data(data)
    return redirect("/")

@app.route("/comment", methods=["POST"])
def comment():
    key = request.form.get("key", "")
    message = request.form.get("comment", "").strip()
    if ":" not in key or not message:
        return "Invalid comment", 400
    kind, filename = key.split(":", 1)
    if kind not in FOLDERS or not os.path.isfile(os.path.join(FOLDERS[kind], filename)):
        return "Not found", 404
    data = load_data()
    data["comments"].setdefault(key, []).append(message[:300])
    save_data(data)
    return redirect("/")

@app.route("/notify", methods=["POST"])
@admin_required
def notify():
    message = request.form.get("text", "").strip()
    if message:
        data = load_data()
        data["notifications"].insert(0, {
            "text": message[:300],
            "date": datetime.now().strftime("%d-%m-%Y %I:%M %p")
        })
        data["notifications"] = data["notifications"][:20]
        save_data(data)
    return redirect("/")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()
    if name and message:
        data = load_data()
        data["messages"].insert(0, {
            "text": name[:50] + ": " + message[:1000],
            "date": datetime.now().strftime("%d-%m-%Y %I:%M %p")
        })
        data["messages"] = data["messages"][:100]
        save_data(data)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
PY
