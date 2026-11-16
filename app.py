
from flask import (
    Flask, request, redirect, url_for, render_template_string,
    session, send_from_directory
)
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime
import os
import json
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "pluto-gaming-secret")

ADMIN_PASSWORD = "ambadijayesh"

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"
DATA_FILE = "data.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

INSTAGRAMS = [
    {
        "name": "@Pluto_ser_her",
        "url": "https://www.instagram.com/Pluto_ser_her/"
    },
    {
        "name": "@_kerala_kings_2027",
        "url": "https://www.instagram.com/_kerala_kings_2027/"
    },
    {
        "name": "@_psycho_ssss",
        "url": "https://www.instagram.com/_psycho_ssss/"
    }
]

ALLOWED_EXTENSIONS = {
    "png", "jpg", "jpeg", "gif", "webp",
    "mp4", "webm", "mov"
}


def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "posts": [],
            "notifications": [],
            "messages": [],
            "likes": {},
            "comments": {}
        }

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        data = {}

    data.setdefault("posts", [])
    data.setdefault("notifications", [])
    data.setdefault("messages", [])
    data.setdefault("likes", {})
    data.setdefault("comments", {})

    return data


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper


def render_page(page, **kwargs):
    data = load_data()

    return render_template_string(
        HTML,
        page=page,
        admin=session.get("admin", False),
        instagrams=INSTAGRAMS,
        posts=data["posts"],
        notifications=data["notifications"],
        messages=data["messages"],
        likes=data["likes"],
        comments=data["comments"],
        **kwargs
    )


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PLUTO GAMING</title>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: #080714;
    color: white;
    font-family: Arial, sans-serif;
    text-align: center;
}

.background-video {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    z-index: -3;
    opacity: 0.22;
}

.overlay {
    position: fixed;
    inset: 0;
    background: rgba(8, 7, 20, 0.72);
    z-index: -2;
}

header {
    background: linear-gradient(
        120deg, rgba(37,0,79,.95), rgba(80,0,160,.95)
    );
    padding: 45px 10px;
}

h1 {
    color: #00eaff;
    font-size: 30px;
    margin: 0 0 18px;
}

.subtitle {
    font-size: 12px;
    letter-spacing: 1px;
}

.container {
    max-width: 600px;
    margin: 30px auto;
    padding: 0 15px;
}

.card {
    background: rgba(25,23,44,.94);
    margin: 15px 0;
    padding: 25px 15px;
    border-radius: 15px;
    border: 1px solid #34245c;
}

.card h2 {
    font-size: 19px;
    margin-bottom: 20px;
    color: #00eaff;
}

.card p {
    color: #ddd;
    font-size: 14px;
}

.btn {
    display: inline-block;
    background: #7025ff;
    color: white;
    padding: 13px 22px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 13px;
    margin: 5px;
    border: none;
    cursor: pointer;
}

.btn:active {
    background: #4c00c9;
}

input, textarea {
    width: 95%;
    padding: 12px;
    margin: 8px 0;
    border: 1px solid #7025ff;
    border-radius: 8px;
    background: #080714;
    color: white;
}

.search {
    width: 95%;
    padding: 14px;
    border-radius: 10px;
    background: #19172c;
    color: white;
    border: 1px solid #7025ff;
}

.post img, .post video {
    width: 100%;
    max-height: 350px;
    object-fit: contain;
    border-radius: 10px;
    margin-top: 10px;
}

.post {
    background: #100e20;
    border-radius: 12px;
    padding: 15px;
    margin: 15px 0;
    overflow-wrap: anywhere;
}

.post p {
    color: white;
}

.comment {
    background: #25213b;
    padding: 8px;
    margin: 5px;
    border-radius: 8px;
    text-align: left;
}

footer {
    color: #888;
    padding: 20px;
    font-size: 12px;
}

.red-particle {
    position: fixed;
    width: 4px;
    height: 4px;
    background: red;
    border-radius: 50%;
    box-shadow: 0 0 10px red;
    pointer-events: none;
    z-index: 5;
    animation: particle 5s linear infinite;
}

@keyframes particle {
    from {
        transform: translateY(100vh);
        opacity: 1;
    }
    to {
        transform: translateY(-20px);
        opacity: 0;
    }
}

a {
    color: #00eaff;
}

</style>
</head>

<body>

<video class="background-video" autoplay muted loop playsinline>
    <source src="/static/background.mp4" type="video/mp4">
</video>
<div class="overlay"></div>

<header>
    <h1>PLUTO GAMING</h1>
    <div class="subtitle">WELCOME TO MY GAMING WORLD</div>
</header>

<div class="container">

{% if page == "home" %}

<div class="card">
    <h2>PLUTO SER</h2>
    <p>Official Gaming Website</p>
    <p>BGMI | GAMING | ENTERTAINMENT</p>
</div>

<div class="card">
    <h2>INSTAGRAM ACCOUNTS</h2>
    <p>Follow our Instagram accounts</p>
    {% for account in instagrams %}
        <a class="btn" href="{{ account.url }}" target="_blank">
            {{ account.name }}
        </a>
    {% endfor %}
</div>

<div class="card">
    <h2>SEARCH GAMING POSTS</h2>
    <input class="search" id="search"
           placeholder="Search gaming posts..."
           oninput="searchPosts()">
</div>

<div class="card">
    <h2>NOTIFICATIONS</h2>
    {% for n in notifications %}
        <p>🔔 {{ n.text }}</p>
    {% else %}
        <p>No notifications yet.</p>
    {% endfor %}
</div>

<div class="card">
    <h2>GAMING GALLERY</h2>

    {% for post in posts %}
    <div class="post searchable">
        <h3>{{ post.title }}</h3>
        <p>{{ post.caption }}</p>

        {% if post.type == "video" %}
            <video controls>
                <source src="/{{ post.file }}">
            </video>
        {% else %}
            <img src="/{{ post.file }}" alt="Gaming image">
        {% endif %}

        <p>❤️ {{ likes.get(post.id, 0) }}</p>

        <form method="POST"
              action="{{ url_for('like_post', post_id=post.id) }}">
            <button class="btn">LIKE</button>
        </form>

        <form method="POST"
              action="{{ url_for('comment_post', post_id=post.id) }}">
            <input name="comment" placeholder="Write a comment..." required>
            <button class="btn">COMMENT</button>
        </form>

        {% for c in comments.get(post.id, []) %}
            <div class="comment">{{ c }}</div>
        {% endfor %}
<form action="{{ url_for('delete_post', post_id=post.id) }}" method="POST"
      onsubmit="return confirm('Are you sure you want to delete this post?');">
    <button type="submit"
            style="background:red;color:white;padding:10px 20px;border:none;border-radius:8px;cursor:pointer;">
        🗑 DELETE POST
    </button>
</form>

    </div>
    {% else %}
        <p>Coming Soon...</p>
    {% endfor %}
</div>

<div class="card">
    <h2>CONTACT ADMIN</h2>
    <form method="POST" action="{{ url_for('contact') }}">
        <input name="name" placeholder="Your name" required>
        <textarea name="message" placeholder="Your message"
                  required></textarea>
        <button class="btn">SEND MESSAGE</button>
    </form>
</div>

{% elif page == "login" %}

<div class="card">
    <h2>ADMIN LOGIN</h2>
    <form method="POST">
        <input type="password" name="password"
               placeholder="Admin password" required>
        <button class="btn">LOGIN</button>
    </form>
</div>

{% elif page == "admin" %}

<div class="card">
    <h2>ADMIN PANEL</h2>
    <p>Welcome Admin</p>
    <a class="btn" href="{{ url_for('home') }}">HOME</a>
    <a class="btn" href="{{ url_for('logout') }}">LOGOUT</a>
</div>

<div class="card">
    <h2>UPLOAD GAMING PHOTO / VIDEO</h2>
    <form method="POST" action="{{ url_for('upload') }}"
          enctype="multipart/form-data">
        <input name="title" placeholder="Post title" required>
        <textarea name="caption" placeholder="Post caption"></textarea>
        <input type="file" name="file" accept="image/*,video/*" required>
        <button class="btn">UPLOAD</button>
    </form>
</div>

<div class="card">
    <h2>ADD NOTIFICATION</h2>
    <form method="POST" action="{{ url_for('add_notification') }}">
        <input name="text" placeholder="Notification text" required>
        <button class="btn">ADD NOTIFICATION</button>
    </form>
</div>

<div class="card">
    <h2>CONTACT MESSAGES</h2>
    {% for m in messages %}
        <div class="comment">
            <b>{{ m.name }}</b>
            <p>{{ m.message }}</p>
            <small>{{ m.date }}</small>
        </div>
    {% else %}
        <p>No messages.</p>
    {% endfor %}
</div>

{% endif %}

</div>

<footer>PLUTO GAMING © 2026</footer>

<script>
function searchPosts() {
    let value = document.getElementById("search").value.toLowerCase();

    document.querySelectorAll(".searchable").forEach(function(post) {
        post.style.display =
            post.innerText.toLowerCase().includes(value) ? "" : "none";
    });
}

for (let i = 0; i < 20; i++) {
    let particle = document.createElement("div");
    particle.className = "red-particle";
    particle.style.left = Math.random() * 100 + "vw";
    particle.style.animationDelay = Math.random() * 5 + "s";
    document.body.appendChild(particle);
}
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_page("home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        return render_page("login", error="Wrong password")

    return render_page("login")


@app.route("/admin")
@admin_required
def admin():
    return render_page("admin")


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))


@app.route("/upload", methods=["POST"])
@admin_required
def upload():
    file = request.files.get("file")

    if not file or not file.filename:
        return redirect(url_for("admin"))

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext not in ALLOWED_EXTENSIONS:
        return "File type not allowed", 400

    new_name = str(uuid.uuid4()) + "." + ext
    file.save(os.path.join(UPLOAD_FOLDER, new_name))

    data = load_data()

    post_type = "video" if ext in {"mp4", "webm", "mov"} else "image"

    data["posts"].insert(0, {
        "id": str(uuid.uuid4()),
        "title": request.form.get("title", "Gaming Post"),
        "caption": request.form.get("caption", ""),
        "file": "uploads/" + new_name,
        "type": post_type,
        "date": datetime.now().strftime("%d-%m-%Y")
    })

    save_data(data)
    return redirect(url_for("admin"))


@app.route("/like/<post_id>", methods=["POST"])
def like_post(post_id):
    data = load_data()

    if any(p["id"] == post_id for p in data["posts"]):
        data["likes"][post_id] = data["likes"].get(post_id, 0) + 1
        save_data(data)

    return redirect(url_for("home"))


@app.route("/comment/<post_id>", methods=["POST"])
def comment_post(post_id):
    data = load_data()
    comment = request.form.get("comment", "").strip()

    if comment and any(p["id"] == post_id for p in data["posts"]):
        data["comments"].setdefault(post_id, []).append(comment[:500])
        save_data(data)

    return redirect(url_for("home"))


@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()

    if name and message:
        data = load_data()
        data["messages"].append({
            "name": name[:80],
            "message": message[:1000],
            "date": datetime.now().strftime("%d-%m-%Y %H:%M")
        })
        save_data(data)

    return redirect(url_for("home"))


@app.route("/notification", methods=["POST"])
@admin_required
def add_notification():
    text = request.form.get("text", "").strip()

    if text:
        data = load_data()
        data["notifications"].insert(0, {
            "text": text[:300],
            "date": datetime.now().strftime("%d-%m-%Y")
        })
        save_data(data)

    return redirect(url_for("admin"))


@app.route("/delete/<post_id>", methods=["POST"])
@admin_required
def delete_post(post_id):
    data = load_data()

    post = next(
        (p for p in data["posts"] if p["id"] == post_id),
        None
    )

    if post:
        data["posts"] = [
            p for p in data["posts"] if p["id"] != post_id
        ]
        data["likes"].pop(post_id, None)
        data["comments"].pop(post_id, None)

        filepath = post.get("file", "")
        if filepath.startswith("uploads/"):
            try:
                os.remove(filepath)
            except OSError:
                pass

        save_data(data)

    return redirect(url_for("admin"))


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

