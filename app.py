import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


LIKES_FILE = "likes.json"

def load_likes():
    with open(LIKES_FILE, "r") as f:
        return json.load(f)

def save_likes(likes):
    with open(LIKES_FILE, "w") as f:
        json.dump(likes, f)

@app.route("/like/<projet_id>", methods=["POST"])
def like(projet_id):
    likes = load_likes()
    action = request.json.get("action")  # "like" ou "unlike"

    if projet_id not in likes:
        likes[projet_id] = 0

    if action == "like":
        likes[projet_id] += 1
    elif action == "unlike" and likes[projet_id] > 0:
        likes[projet_id] -= 1

    save_likes(likes)
    return jsonify({"likes": likes[projet_id]})

@app.route("/likes")
def get_likes():
    likes = load_likes()
    return jsonify(likes)

@app.route('/')
def home():
    return render_template('index.html', title="Accueil – Depp3D")

@app.route('/tests')
def tests():
    return render_template('tests.html', title="Tests – Depp3D")

@app.route('/impressions')
def impressions():
    return render_template('impressions.html', title="Impressions 3D – Depp3D")

@app.route('/projet/<nom>')
def projet(nom):
    try:
        return render_template(f"projet/{nom}.html")
    except:
        return render_template("404.html"), 404
    
@app.route("/articles")
def articles():
    return render_template("articles.html")

@app.route("/articles/<slug>")
def article(slug):
    return render_template(f"articles/{slug}.html")

@app.route("/guide/<slug>")
def guide_article(slug):
    return render_template(f"guide/{slug}.html")

@app.route("/news/<slug>")
def news_article(slug):
    return render_template(f"news/{slug}.html")

@app.route('/tests/<slug>')
def test_article(slug):
    return render_template(f'test/{slug}.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/guide')
def guide():
    return render_template('guide.html')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)