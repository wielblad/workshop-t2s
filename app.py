from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="pl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Global Azure 2025</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8 text-center">
                    <h1 class="mb-4">Witaj na Global Azure 2025!</h1>
                    <p class="lead">To przykładowy frontend z Bootstrapem.</p>
                    {% if session.get('logged_in') %}
                        <p class="text-success">Jesteś zalogowany jako <b>{{ session.get('username') }}</b></p>
                        <a href="{{ url_for('logout') }}" class="btn btn-danger">Wyloguj</a>
                    {% else %}
                        <a href="{{ url_for('login') }}" class="btn btn-primary btn-lg">Zaloguj się</a>
                    {% endif %}
                </div>
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Nieprawidłowy login lub hasło.'
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
                    {% if error %}
                        <div class="alert alert-danger">{{ error }}</div>
                    {% endif %}
                    <form method="post">
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
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    '''
    return render_template_string(html, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)