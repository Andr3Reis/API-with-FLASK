from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

biblioteca = []

def encontrar_livro(livro_id):
    return next((livro for livro in biblioteca if livro["id"] == livro_id), None)

@app.route('/')
def index():
    return render_template('index.html', livros=biblioteca)

@app.route('/form', methods=['GET', 'POST'])
@app.route('/form/<int:livro_id>', methods=['GET', 'POST'])
def form(livro_id=None):
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']

        if livro_id:
            livro = encontrar_livro(livro_id)
            if livro:
                livro['titulo'] = titulo
                livro['autor'] = autor
                livro['ano_publicacao'] = ano_publicacao
        else: 
            novo_livro = {
                "id": len(biblioteca) + 1,
                "titulo": titulo,
                "autor": autor,
                "ano_publicacao": ano_publicacao
            }
            biblioteca.append(novo_livro)
        
        return redirect(url_for('index'))

    livro = encontrar_livro(livro_id) if livro_id else None
    return render_template('form.html', livro=livro)

@app.route('/delete/<int:livro_id>', methods=['POST'])
def deletar_livro(livro_id):
    livro = encontrar_livro(livro_id)
    if livro:
        biblioteca.remove(livro)
    return redirect(url_for('index'))

@app.route('/api/livros', methods=['GET'])
def api_listar_livros():
    return jsonify(biblioteca), 200

@app.route('/api/livros', methods=['POST'])
def api_adicionar_livro():
    if not request.json or not 'titulo' in request.json or not 'autor' in request.json:
        return jsonify({"error": "Dados incompletos"}), 400

    novo_livro = {
        "id": len(biblioteca) + 1,
        "titulo": request.json['titulo'],
        "autor": request.json['autor'],
        "ano_publicacao": request.json.get('ano_publicacao', 0)  # Ano é opcional
    }
    biblioteca.append(novo_livro)
    return jsonify(novo_livro), 201

@app.route('/api/livros/<int:livro_id>', methods=['PUT'])
def api_atualizar_livro(livro_id):
    livro = encontrar_livro(livro_id)
    if not livro:
        return jsonify({"error": "Livro não encontrado"}), 404
    
    if not request.json:
        return jsonify({"error": "Nenhum dado fornecido"}), 400
    
    livro['titulo'] = request.json.get('titulo', livro['titulo'])
    livro['autor'] = request.json.get('autor', livro['autor'])
    livro['ano_publicacao'] = request.json.get('ano_publicacao', livro['ano_publicacao'])

    return jsonify(livro), 200

@app.route('/api/livros/<int:livro_id>', methods=['DELETE'])
def api_deletar_livro(livro_id):
    livro = encontrar_livro(livro_id)
    if not livro:
        return jsonify({"error": "Livro não encontrado"}), 404
    
    biblioteca.remove(livro)
    return jsonify({"message": "Livro deletado"}), 200

if __name__ == '__main__':
    app.run(debug=True)
