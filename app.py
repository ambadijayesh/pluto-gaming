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
body { margin:0; background:#080714; color:white; font-family:Arial; }
header { background:#17132b; padding:25px; text-align:center; border-bottom:2px solid #8b5cf6; }
header h1 { color:#a78bfa; margin:0; }
.container { padding:18px; max-width:800px; margin:auto; }
.card { background:#17152b; padding:18px; margin:15px 0; border-radius:14px; }
button { background:#8b5cf6; color:white; border:0; padding:12px 20px; border-radius:8px; font-weight:bold; }
input { max-width:100%; margin:12px 0; }
video { width:100%; border-radius:10px; }
a { color:#c4b5fd; }
</style>
</head>
<body>
<header>
<h1>PLUTO GAMING</h1>
<p>GAMING VIDEOS & HIGHLIGHTS</p>
</header>
<div class="container">
{% if admin %}
<div class="card">
<h2>Upload Video (Admin Only)</h2>
<form action="/upload" method="POST" enctype="multipart/form-data">
<input type="file" name="video" accept="video/*" required>
<br><button type="submit">UPLOAD VIDEO</button>
</form>
<a href="/logout">Logout</a>
</div>
{% else %}
<div class="card">
<h2>Admin Login</h2>
<form action="/login" method="POST">
<input type="password" name="password" placeholder="Admin password" required>
<br><button type="submit">LOGIN</button>
</form>
</div>
{% endif %}
<div class="card">
<h2>Instagram</h2>
<a href="https://www.instagram.com/pluto_ser_her/" target="_blank">
<button>VISIT INSTAGRAM</button>
</a>
</div>
<h2>Video Gallery</h2>
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
