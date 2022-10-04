from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/teste')
def teste():
    return render_template('teste.html')

@app.route('/produtos')
def produtos():
    return render_template('produtos.html')

if __name__ == '__main__':
    app.run(debug=True)