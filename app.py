import json
from flask import Flask, render_template, request, jsonify, Response

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

@app.route('/robots.txt')
def robots_txt():
    return app.send_static_file('robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    base_url = "https://deep3d.fr"
    pages = [
        "",  # Accueil
        "articles",
        "guide",
        "test",
        "news",
        "projet",
        "impressions",
        "tests",
    ]

    # Ajouter les fichiers HTML dans chaque dossier
    def get_html_slugs(folder, url_prefix):
        slugs = []
        path = os.path.join(app.template_folder, folder)
        if os.path.exists(path):
            for f in os.listdir(path):
                if f.endswith(".html"):
                    name = f.replace(".html", "")
                    slugs.append(f"{url_prefix}/{name}")
        return slugs

    urls = [f"{base_url}/{p}" for p in pages]

    urls += get_html_slugs("articles", f"{base_url}/articles")
    urls += get_html_slugs("guide", f"{base_url}/guide")
    urls += get_html_slugs("test", f"{base_url}/test")
    urls += get_html_slugs("news", f"{base_url}/news")
    urls += get_html_slugs("projet", f"{base_url}/projet")

    # Génération du XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in urls:
        xml += f"  <url>\n    <loc>{url}</loc>\n  </url>\n"
    xml += '</urlset>'

    return Response(xml, mimetype="application/xml")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)