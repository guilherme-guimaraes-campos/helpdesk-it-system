from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT DEFAULT 'Aberto',
            tecnico TEXT DEFAULT 'Não atribuído'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo, descricao, status, tecnico FROM chamado')
    chamados = cursor.fetchall()
    conn.close()
    return render_template('index.html', chamados=chamados)

@app.route('/novo', methods=('GET', 'POST'))
def novo_chamado():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chamado (titulo, descricao) VALUES (?, ?)', (titulo, descricao))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('novo_chamado.html')

@app.route('/fechar/<int:id>')
def fechar_chamado(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE chamado SET status = 'Fechado' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)