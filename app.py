from flask import Flask, render_template,request,redirect
from numpy import empty
import pandas as pd

app = Flask(__name__)

df = pd.read_json('data.json')
produtos = df.to_dict('records')

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/listar_produtos')
def listar():
    global df
    df = pd.read_json('data.json')
    return render_template('listar_produtos.html', produtos = df.to_dict('records') )

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

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


if __name__ == '__main__':
    app.run(debug=True)