
from flask import Flask, render_template_string

app = Flask(__name__)

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

header {
    background: linear-gradient(120deg, #25004f, #5000a0);
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
    max-width: 420px;
    margin: 30px auto;
    padding: 0 15px;
}

.card {
    background: #19172c;
    margin: 15px 0;
    padding: 30px 15px;
    border-radius: 15px;
}

.card h2 {
    font-size: 19px;
    margin-bottom: 20px;
}

.card p {
    color: #ddd;
    font-size: 14px;
}

.btn {
    display: inline-block;
    background: #7025ff;
    color: white;
    padding: 13px 25px;
    border-radius: 8px;
    text-decoration: none;
    font-size: 13px;
    margin-top: 5px;
}

.btn:active {
    background: #4c00c9;
}

footer {
    color: #888;
    padding: 20px;
    font-size: 12px;
}
</style>
</head>

<body>

<header>
    <h1>PLUTO GAMING</h1>
    <div class="subtitle">
        WELCOME TO MY GAMING WORLD
    </div>
</header>

<div class="container">

    <div class="card">
        <h2>PLUTO SER</h2>
        <p>Official Gaming Website</p>
        <p>BGMI | GAMING | ENTERTAINMENT</p>
    </div>

    <div class="card">
        <h2>INSTAGRAM</h2>
        <p>Follow my Instagram account</p>

        <a class="btn"
        href="https://www.instagram.com/Pluto_ser_her/"
        target="_blank">
        VISIT INSTAGRAM
        </a>
    </div>

    <div class="card">
        <h2>GAMING GALLERY</h2>
        <p>Coming Soon...</p>
    </div>

</div>

<footer>
    PLUTO GAMING © 2026
</footer>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

