import math
from random import sample
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


user_words = None
user_number = None


@app.route("/")
@app.route("/first")
def first():
    return render_template('index_first.html')


@app.route("/second", methods=["POST", "GET"])
def second():
    words_error = None
    number_error = None
    error = False
    if request.method == 'POST':
        print(request.form)
        if len(request.form['user_words']) == 0:
            words_error = "Поле не может быть пустым."
            error = True
        if len(request.form['user_number']) == 0:
            number_error = 'Поле не может быть пустым.'
            error = True
        elif request.form['user_number'][0][0] == '-':
            number_error = "Число должно быть неотрицательным"
            error = True
        if error:
            return render_template('index_second.html', words_error=words_error, number_error=number_error)
        else:
            global user_words
            user_words = request.form['user_words'].split(", ")
            global user_number
            user_number = request.form['user_number']
            return redirect(url_for('third'))
    else:
        return render_template('index_second.html', words_error=words_error, number_error=number_error)


@app.route("/third")
def third():
    global user_words
    global user_number
    generated_sentence = generate_sentence(user_words, user_number)
    return render_template('index_third.html', sentence=generated_sentence)


def generate_sentence(words, number):
    number = int(number)
    ex = number / len(words)
    if ex != 0:
        words *= math.ceil(ex)
    return " ".join(sample(words, number))


if __name__ == "__main__":
    app.run(debug=True)
