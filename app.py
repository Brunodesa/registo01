from flask import Flask, render_template, request

app = Flask(__name__)


def gravar(v1, v2, v3):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
    db.execute(" INSERT INTO usr VALUES (?, ?, ?)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()


def existe(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute(" SELECT nome FROM usr WHERE nome = ?", (v1,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def alterar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute(" UPDATE usr SET passe = ? WHERE nome = ?", (v2, v1))
    ficheiro.commit()
    ficheiro.close()


@app.route('/', methods=['GET', 'POST'])
def route():
    print(existe('admin'))
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O utlizador já existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2, v3)
    return render_template('registo.html', erro=erro)


@app.route('/', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if not existe(v1):
            erro = 'O utlizador não existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
    return render_template('newpasse.html', erro=erro)


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        usr = request.form['utilizador']
        passes = usr.passes()
        # Se o utilizador existe e a passe está correta:
        if usr in passes and passes[usr] == usr.code(request.form['passe']):
            usr.set(request.form['utilizador'])
        elif usr not in passes:
            erro = 'O utilizador não existe.'
        else:
            erro = 'A palavra passe está incorreta.'
    return render_template('login.html', erro=erro)


if __name__ == "__main__":
    app.run(debug=True)
