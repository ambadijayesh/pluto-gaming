from flask import Flask, request, redirect, render_template_string, send_from_directory, session
from werkzeug.utils import secure_filename
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ambadijayesh")

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PLUTO GAMING</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }

body {
 margin:0;
 background:#050505;
 color:white;
 font-family:Arial,sans-serif;
 overflow-x:hidden;
}

header {
 text-align:center;
 padding:35px 15px;
 background:linear-gradient(135deg,#080808,#250000,#080808);
 border-bottom:2px solid #ff1010;
 box-shadow:0 0 25px #ff101055;
}

header h1 {
 font-size:38px;
 color:#ff2020;
 letter-spacing:5px;
 text-shadow:0 0 12px red,0 0 30px #ff0000;
 animation:glow 2s infinite alternate;
 margin:0;
}

header p {
 color:#ddd;
 letter-spacing:3px;
 font-size:12px;
}

@keyframes glow {
 from { text-shadow:0 0 8px red; }
 to { text-shadow:0 0 25px red,0 0 45px #ff0000; }
}

.container {
 padding:18px;
 max-width:850px;
 margin:auto;
}

.card {
 background:linear-gradient(145deg,#171717,#090909);
 border:1px solid #5b0808;
 padding:20px;
 margin:18px 0;
 border-radius:12px;
 box-shadow:0 0 15px #ff000022;
 animation:fade 1s ease;
}

@keyframes fade {
 from {opacity:0;transform:translateY(15px);}
 to {opacity:1;transform:translateY(0);}
}

h2 {
 color:#ff3030;
 text-transform:uppercase;
}

button {
 background:linear-gradient(90deg,#8b0000,#ff1717);
 color:white;
 border:1px solid #ff5555;
 padding:13px 22px;
 border-radius:7px;
 font-weight:bold;
 cursor:pointer;
 box-shadow:0 0 12px #ff000044;
}

button:hover {
 transform:scale(1.04);
 box-shadow:0 0 22px red;
}

input {
 max-width:100%;
 margin:12px 0;
 padding:10px;
 background:#171717;
 color:white;
 border:1px solid #aa1515;
 border-radius:6px;
}

video {
 width:100%;
 border-radius:10px;
 border:1px solid #ff2525;
}

a {color:#ff5555;text-decoration:none;}

.section-title {
 border-left:4px solid red;
 padding-left:12px;
 margin-top:30px;
}

.tag {
 display:inline-block;
 color:#ff3030;
 border:1px solid #ff3030;
 padding:7px 12px;
 margin:5px;
 border-radius:20px;
 font-size:12px;
}

footer {
 text-align:center;
 padding:25px;
 color:#777;
 border-top:1px solid #5b0808;
}

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

{% if admin %}
<div class="card">
<h2>Admin Dashboard</h2>
<form action="/upload" method="POST" enctype="multipart/form-data">
<input type="file" name="video" accept="video/*" required>
<br>
<button type="submit">UPLOAD VIDEO</button>
</form>
<a href="/logout">Logout</a>
</div>
{% else %}
<div class="card">
<h2>Admin Login</h2>
<form action="/login" method="POST">
<input type="password" name="password" placeholder="Admin password" required>
<br>
<button type="submit">LOGIN</button>
</form>
</div>
{% endif %}

<div class="card">
<h2>Instagram</h2>
<a href="https://www.instagram.com/pluto_ser_her/" target="_blank">
<button>VISIT INSTAGRAM</button>
</a>
</div>

<h2 class="section-title">Video Gallery</h2>

{% for video in videos %}
<div class="card">
<video controls preload="metadata">
<source src="/videos/{{ video }}">
</video>
<p>{{ video }}</p>
</div>
{% else %}
<div class="card">No videos uploaded yet.</div>
{% endfor %}

</div>

<footer>
PLUTO GAMING © 2026
</footer>

</body>
</html>
"""

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

@app.route("/")
def home():
    videos = sorted(os.listdir(UPLOAD_FOLDER), reverse=True)
    return render_template_string(HTML, videos=videos, admin=session.get("admin", False))

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
    file = request.files.get("video")
    if not file or not file.filename:
        return "Please select a video", 400

    filename = secure_filename(file.filename)
    if not filename.lower().endswith((".mp4", ".webm", ".mov", ".mkv")):
        return "Video files only", 400

    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return redirect("/")

@app.route("/videos/<path:filename>")
def videos(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

