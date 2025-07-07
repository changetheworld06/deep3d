import json
from flask import Flask, render_template, request, jsonify, Response, send_from_directory
import os
from datetime import datetime

# 👉 Ici tu initialises ton app Flask
app = Flask(__name__, template_folder="templates")


LIKES_FILE = "likes.json"

def load_likes():
    with open(LIKES_FILE, "r") as f:
        return json.load(f)

def save_likes(likes):
    with open(LIKES_FILE, "w") as f:
        json.dump(likes, f)

@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com https://pagead2.googlesyndication.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
        "font-src 'self' https://fonts.gstatic.com; "
        "frame-src https://*.doubleclick.net https://*.googlesyndication.com; "
        "connect-src 'self' https://www.google-analytics.com; "
    )
    response.headers['Strict-Transport-Security'] = "max-age=31536000; includeSubDomains"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "DENY"
    response.headers['Referrer-Policy'] = "no-referrer"
    response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()"
    return response

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

@app.route("/mentions-legales")
def mentions_legales():
    return render_template("mentions-legales.html")

@app.route("/confidentialite")
def politique_confidentialite():
    return render_template("confidentialite.html")

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico')

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/ads.txt')
def ads():
    return send_from_directory('static', 'ads.txt')

@app.route('/sitemap.xml')
def sitemap():
    base_url = "https://deep3d.fr"
    today = datetime.utcnow().date().isoformat()

    # Pages principales
    static_pages = [
        "",  # Accueil
        "articles",
        "guide",
        "news",
        "impressions",
        "tests"
    ]

    # Convertit les pages fixes en URLs complètes avec date
    urls = [{"loc": f"{base_url}/{page}", "lastmod": today} for page in static_pages]

    # Dictionnaire des dossiers dynamiques et leurs chemins URL
    dynamic_dirs = {
        "articles": f"{base_url}/articles",
        "news": f"{base_url}/news",
        "guide": f"{base_url}/guide",
        "test": f"{base_url}/test",
        "projet": f"{base_url}/projet"
    }

    # Ajoute les fichiers HTML dynamiques comme pages individuelles
    for folder, url_prefix in dynamic_dirs.items():
        path = os.path.join(app.template_folder, folder)
        if os.path.exists(path):
            for filename in os.listdir(path):
                if filename.endswith(".html"):
                    slug = filename.replace(".html", "")
                    full_url = f"{url_prefix}/{slug}"
                    urls.append({
                        "loc": full_url,
                        "lastmod": today
                    })

    # Génère le sitemap XML
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    for entry in urls:
        xml += "  <url>\n"
        xml += f"    <loc>{entry['loc']}</loc>\n"
        xml += f"    <lastmod>{entry['lastmod']}</lastmod>\n"
        xml += "  </url>\n"

    xml += '</urlset>'

    return Response(xml, mimetype='application/xml')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)