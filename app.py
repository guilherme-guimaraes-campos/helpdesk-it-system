from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Cria a tabela apenas se não existir (sem apagar dados anteriores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            solicitante TEXT NOT NULL,
            status TEXT DEFAULT 'Aberto',
            tecnico TEXT DEFAULT 'Não atribuído',
            resolucao TEXT DEFAULT ''
        )
    ''')
    conn.commit()
    conn.close()

# Executa a inicialização ao carregar o aplicativo
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo, descricao, solicitante, status, tecnico, resolucao FROM chamado')
    chamados = cursor.fetchall()
    conn.close()
    return render_template('index.html', chamados=chamados)

@app.route('/novo', methods=('GET', 'POST'))
def novo_chamado():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        solicitante = request.form['solicitante']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO chamado (titulo, descricao, solicitante) VALUES (?, ?, ?)', (titulo, descricao, solicitante))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('novo_chamado.html')

@app.route('/fechar/<int:id>', methods=('GET', 'POST'))
def fechar_chamado(id):
    if request.method == 'POST':
        resolucao = request.form['resolucao']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE chamado SET status = 'Fechado', resolucao = ? WHERE id = ?", (resolucao, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, titulo, descricao, solicitante FROM chamado WHERE id = ?', (id,))
    chamado = cursor.fetchone()
    conn.close()
    return render_template('fechar_chamado.html', chamado=chamado)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)