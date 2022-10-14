from flask import Flask, render_template,request,redirect, flash
from numpy import empty
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

df = pd.read_json('data.json')
produtos = df.to_dict('records')

Carrinho = pd.DataFrame([])
Relatorio = pd.DataFrame([])

@app.route('/')
def index():
    return render_template('home.html', carrinho = Carrinho.to_dict('records'))

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/listar_produtos')
def listar():
    global df
    df = pd.read_json('data.json')
    return render_template('listar_produtos.html', produtos = df.to_dict('records'), carrinho = Carrinho.to_dict('records') )

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html', carrinho = Carrinho.to_dict('records'))

@app.route('/cadastrado')#/adicionar?produto=valor&preco=valor
def cadastrado():
    global df
    argumentos = request.args.to_dict(True)
    #print(argumentos)
    if df.empty:
        argumentos['id'] = [1]
    else:
        argumentos['id'] = [df['id'].max() + 1]
    df = pd.concat([df, pd.DataFrame(argumentos)], ignore_index=True)
    df.to_json('data.json', orient='records')
    return redirect('/cadastro')

@app.route('/deletar/<id>')
def deletar(id):
    mask_id = df[df['id'] == int(id)].index
    df.drop(mask_id, axis=0, inplace=True)
    df.to_json('data.json', orient='records')
    return redirect('/listar_produtos')

#Vendas carrinho ========================================================    

@app.route('/vendas')
def vendas():
    global df
    df = pd.read_json('data.json')
    return render_template('/vendas.html', produtos = df.to_dict('records'), carrinho = Carrinho.to_dict('records'))

@app.route('/adicionar/<id>')
def adicionarCarrinho(id):
    global Carrinho
    mask_id = df[df['id'] == int(id)]
    Carrinho = pd.concat([Carrinho, mask_id])
    # print(Carrinho)
    print(mask_id.nome.values[0])
    flash(f"Olá você adicionou o produto {mask_id.nome.values[0]} com sucesso!")
    return redirect('/vendas')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html', carrinho = Carrinho.to_dict('records'))

@app.route('/deletarCarrinho/<id>')
def deletarCarrinho(id):
    mask_id = Carrinho[Carrinho['id'] == int(id)].index
    Carrinho.drop(mask_id, axis=0, inplace=True)
    return redirect('/carrinho')

@app.route('/gerarRelatorio')
def gerarRelatorio():
    global Relatorio
    global Carrinho
    Relatorio = pd.concat([Relatorio, Carrinho.copy()])
    Carrinho = pd.DataFrame([])
    print(Relatorio)
    return redirect('/carrinho')
#=====================================================

@app.route('/relatorio')
def relatorio():
    return render_template('relatorio.html', relatorio = Relatorio.to_dict('records'), carrinho = Carrinho.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True)