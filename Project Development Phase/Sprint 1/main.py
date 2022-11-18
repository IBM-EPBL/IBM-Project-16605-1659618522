from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login_page.html')


@app.route('/Register_page')
def Register_page():
    return render_template('Register_page.html')

if __name__ == '__main__':
   app.run(debug=True)