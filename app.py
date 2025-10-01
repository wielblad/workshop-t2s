from flask import Flask, render_template_string, request, redirect, url_for, session
import psycopg2


app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dekorator wymagający logowania
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Konfiguracja połączenia z bazą PostgreSQL
DB_HOST = "postgresql-server-postgres-user04.postgres.database.azure.com"
DB_NAME = "usersdb"
DB_USER = "pgadmin"
DB_PASS = "admin"


@app.route('/')
@login_required
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Global Azure 2025</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                min-height: 100vh;
                background: linear-gradient(135deg, #4f8cff 0%, #6ee2f5 100%);
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            }
            .main-card {
                background: #fff;
                border-radius: 1.5rem;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
                padding: 2.5rem 2rem;
                margin-top: 4rem;
                margin-bottom: 2rem;
                transition: box-shadow 0.3s;
            }
            .main-card:hover {
                box-shadow: 0 16px 48px 0 rgba(31, 38, 135, 0.25);
            }
            .menu-btns a {
                min-width: 140px;
                font-size: 1.1rem;
                border-radius: 2rem;
                box-shadow: 0 2px 8px rgba(79,140,255,0.08);
                margin: 0.3rem;
            }
            .azure-title {
                background: linear-gradient(90deg, #4f8cff, #6ee2f5);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 700;
                font-size: 2.7rem;
                margin-bottom: 1.2rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="row justify-content-center">
                <div class="col-lg-7 col-md-9">
                    <div class="main-card text-center">
                        <div class="azure-title">Witaj na Global Azure 2025!</div>
                        <p class="lead mb-4">Nowoczesny frontend z Bootstrapem i gradientem Azure.</p>
                        {% if session.get('logged_in') %}
                            <p class="text-success">Jesteś zalogowany jako <b>{{ session.get('username') }}</b></p>
                            <div class="menu-btns mb-4">
                                <a href="{{ url_for('blog') }}" class="btn btn-outline-primary">Blog</a>
                                <a href="{{ url_for('add_post') }}" class="btn btn-outline-success">Dodaj post</a>
                                <a href="{{ url_for('logout') }}" class="btn btn-danger">Wyloguj</a>
                            </div>
                        {% else %}
                            <a href="{{ url_for('login') }}" class="btn btn-primary btn-lg menu-btns">Zaloguj się</a>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html)



 # Widok logowania z XHR
@app.route('/login', methods=['GET'])
def login():
    html = '''
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Logowanie</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <h2 class="mb-4 text-center">Logowanie</h2>
                    <div id="error" class="alert alert-danger d-none"></div>
                    <form id="loginForm">
                        <div class="mb-3">
                            <label for="username" class="form-label">Login</label>
                            <input type="text" class="form-control" id="username" name="username" required>
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Hasło</label>
                            <input type="password" class="form-control" id="password" name="password" required>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Zaloguj się</button>
                    </form>
                </div>
            </div>
        </div>
        <script>
        document.getElementById('loginForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            if (data.success) {
                window.location.href = '/';
            } else {
                const errorDiv = document.getElementById('error');
                errorDiv.textContent = data.error;
                errorDiv.classList.remove('d-none');
            }
        });
        </script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html)

# Endpoint API do logowania
from flask import jsonify
@app.route('/api/login', methods=['POST'])
def api_login():
    if not request.is_json:
        return jsonify({'success': False, 'error': 'Request musi być typu application/json'}), 400
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': 'Brak danych w żądaniu'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Brak loginu lub hasła'}), 400
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'Nieprawidłowy login lub hasło.'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Błąd połączenia z bazą: {e}'})


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('home') )



# Wyświetlanie wszystkich postów z komentarzami
@app.route('/blog')
@login_required
def blog():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("SELECT p.id, p.title, p.content, u.username, p.created_at FROM posts p LEFT JOIN users u ON p.user_id = u.id ORDER BY p.created_at DESC")
        posts = cur.fetchall()
        post_list = []
        for post in posts:
            cur.execute("SELECT c.content, u.username, c.created_at FROM comments c LEFT JOIN users u ON c.user_id = u.id WHERE c.post_id = %s ORDER BY c.created_at ASC", (post[0],))
            comments = cur.fetchall()
            post_list.append({
                'id': post[0],
                'title': post[1],
                'content': post[2],
                'author': post[3],
                'created_at': post[4],
                'comments': comments
            })
        cur.close()
        conn.close()
    except Exception as e:
        post_list = []
        error = str(e)
    else:
        error = None
    html = '''
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Blog</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">Blog</h1>
            {% if session.get('logged_in') %}
                <a href="{{ url_for('add_post') }}" class="btn btn-success mb-4">Dodaj nowy post</a>
            {% endif %}
            {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
            {% endif %}
            {% for post in posts %}
                <div class="card mb-4">
                    <div class="card-body">
                        <h4>{{ post.title }}</h4>
                        <p>{{ post.content }}</p>
                        <p class="text-muted">Autor: {{ post.author or 'Anonim' }} | {{ post.created_at }}</p>
                        <hr>
                        <h6>Komentarze:</h6>
                        {% for comment in post.comments %}
                            <div class="mb-2"><b>{{ comment[1] or 'Anonim' }}:</b> {{ comment[0] }} <span class="text-muted">{{ comment[2] }}</span></div>
                        {% endfor %}
                        {% if session.get('logged_in') %}
                            <form method="post" action="{{ url_for('add_comment', post_id=post.id) }}">
                                <div class="input-group mb-2">
                                    <input type="text" name="content" class="form-control" placeholder="Dodaj komentarz..." required>
                                    <button class="btn btn-primary" type="submit">Dodaj</button>
                                </div>
                            </form>
                        {% endif %}
                    </div>
                </div>
            {% endfor %}
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html, posts=post_list, error=error)


# Dodawanie nowego posta
@app.route('/blog/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                sslmode="require"
            )
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username=%s", (session.get('username'),))
            user = cur.fetchone()
            user_id = user[0] if user else None
            cur.execute("INSERT INTO posts (user_id, title, content) VALUES (%s, %s, %s)", (user_id, title, content))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('blog'))
        except Exception as e:
            error = str(e)
    html = '''
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Dodaj post</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h2>Dodaj nowy post</h2>
            {% if error %}
                <div class="alert alert-danger">{{ error }}</div>
            {% endif %}
            <form method="post">
                <div class="mb-3">
                    <label for="title" class="form-label">Tytuł</label>
                    <input type="text" class="form-control" id="title" name="title" required>
                </div>
                <div class="mb-3">
                    <label for="content" class="form-label">Treść</label>
                    <textarea class="form-control" id="content" name="content" rows="5" required></textarea>
                </div>
                <button type="submit" class="btn btn-success">Dodaj post</button>
            </form>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html, error=error)


# Dodawanie komentarza do posta
@app.route('/blog/comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    content = request.form.get('content')
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=%s", (session.get('username'),))
        user = cur.fetchone()
        user_id = user[0] if user else None
        cur.execute("INSERT INTO comments (post_id, user_id, content) VALUES (%s, %s, %s)", (post_id, user_id, content))
        conn.commit()
        cur.close()
        conn.close()
    except Exception:
        pass
    return redirect(url_for('blog'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)