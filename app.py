from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_json('data.json')
Produtos = df.to_dict('records')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

@app.route('/teste_produtos')
def teste_produtos():
    return render_template('teste_produto.html', produtos = Produtos)

if __name__ == '__main__':
    app.run(debug=True)