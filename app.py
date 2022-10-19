from flask import Flask, render_template,request,redirect, flash
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
    df = pd.read_json('data.json')
    quantidade = int(request.args['quantidade'])
    mask = df[df['id'] == int(id)]
    mask2 = df['id'] == int(id)
    nomeWeb = mask.values[0][1] # mask.values é um array dentro de um array
    if mask.quantidade.values[0] > 0:
        if Carrinho.empty:# se o carrinho estiver vazio
            id = 1
            produto = {"id": id , "nome": mask.nome.values[0], "preco": mask.preco.values[0], "quantidade": quantidade}
            Carrinho = Carrinho.append(produto, ignore_index=True)
            flash(f"Você adicionou o produto {mask.nome.values[0]} com sucesso!")
            df.loc[mask2, 'quantidade'] =  df.loc[mask2, 'quantidade'].values[0] - quantidade #diminuir quantidade produto
            print(df)
        else:
            maskNome = Carrinho['nome'] == nomeWeb
            if Carrinho[maskNome].empty:
                id = Carrinho['id'].max() + 1
                produto = {"id": id , "nome": mask.nome.values[0], "preco": mask.preco.values[0], "quantidade": quantidade}
                Carrinho = Carrinho.append(produto, ignore_index=True)
                flash(f"Você adicionou o produto {mask.nome.values[0]} com sucesso!")
                df.loc[mask2, 'quantidade'] =  df.loc[mask2, 'quantidade'].values[0] - quantidade
                print(df)
            else:
                print("Pois é")
                Carrinho.loc[maskNome, 'quantidade'] = Carrinho[maskNome]["quantidade"].values[0] + quantidade
                df.loc[mask2, 'quantidade'] =  df.loc[mask2, 'quantidade'].values[0] - quantidade
                flash(f"Você adicionou o produto {mask.nome.values[0]} com sucesso!")
                print(df)
    else:
        print("Não deu")
    df.to_json('data.json', orient='records')
    return redirect('/vendas')
    # # mask_id = df[df['id'] == int(id)]
    # # Carrinho = pd.concat([Carrinho, mask_id])
    # # # print(Carrinho)
    # # print(mask_id.nome.values[0])
    # # flash(f"Olá você adicionou o produto {mask_id.nome.values[0]} com sucesso!")
    # # return redirect('/vendas')

@app.route('/carrinho')
def carrinho():
    total = 0
    carrinho_dict = Carrinho.to_dict('records')
    for produto in carrinho_dict:
        total = total + produto["quantidade"] * produto["preco"]
    return render_template('carrinho.html', carrinho = Carrinho.to_dict('records'), total = total)

@app.route('/deletarCarrinho/<id>')
def deletarCarrinho(id):
    mask_id = Carrinho[Carrinho['id'] == int(id)].index   
#=======================================================================
    mask = Carrinho['id'] == int(id)
    nomeWeb = Carrinho[mask].values[0][1]
    maskNome = df['nome'] == nomeWeb
    
    print(df.loc[maskNome, 'quantidade'].values[0])
    quantidadeCarrinho = Carrinho[mask]["quantidade"].values[0]

    df.loc[maskNome, 'quantidade'] =  df.loc[maskNome, 'quantidade'].values[0] + quantidadeCarrinho
#========================================================================
    Carrinho.drop(mask_id, axis=0, inplace=True)
    df.to_json('data.json', orient='records')
    return redirect('/carrinho')

@app.route('/gerarRelatorio')
def gerarRelatorio():
    global Relatorio
    global Carrinho
    carrinho_dict = Carrinho.to_dict('records')
    if Relatorio.empty:
     Relatorio = pd.concat([Relatorio, Carrinho])
    else:
        for produto in carrinho_dict:
            resultado = Relatorio['nome'] == produto['nome']
            if Relatorio[resultado].empty:
                print("Não tem!")
                Relatorio = pd.concat([Relatorio, pd.DataFrame(produto, index=[0])], ignore_index=True) #sem o index =[0] da erro
            else:
                print("Ok, esse existe")
                Relatorio.loc[resultado, "quantidade"] = Relatorio[resultado]["quantidade"].values[0] + produto['quantidade']  
    Carrinho = pd.DataFrame([]) 
    # global Relatorio
    # global Carrinho
    # Relatorio = pd.concat([Relatorio, Carrinho.copy()])
    # Carrinho = pd.DataFrame([])
    # print(Relatorio)
    return redirect('/carrinho')
#=====================================================

@app.route('/relatorio')
def relatorio():
    global Relatorio
    relatorio_dict = Relatorio.to_dict('records')
    total = 0
    for produto in relatorio_dict:
        total = total + produto["quantidade"] * produto["preco"]
    return render_template('relatorio.html', 
    relatorio = Relatorio.to_dict('records'), carrinho = Carrinho.to_dict('records'),
    total=total) 

if __name__ == '__main__':
    app.run(debug=True)