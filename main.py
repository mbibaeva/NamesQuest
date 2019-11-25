
import os
os.system('pip3.7 install --user wordcloud')
os.system('pip3.7 install --user request')

from flask import Flask
from flask import render_template, request, redirect, url_for
import mysite.handler as handler
import pandas as pd

app = Flask(__name__)
tools = handler.Tools()

@app.route('/', methods = ['post', 'get'])
def questionnaire():
    if request.form:
        the_name = request.form['nfull']
        groupid = tools.save_res(request.form)
        answers_num, cloud_name = tools.create_visuals_ind(the_name, groupid)
        return render_template('your_results.html', the_name = the_name, answers_num = answers_num, cloud_name = cloud_name)
    else:
        print(request.form)
    return render_template('questionnaire.html')


@app.route('/results', methods = ['post', 'get'])
def results():
    names = tools.display_all()
    return render_template('results.html', names1 = names, names2 = names)


if __name__ == '__main__':
    app.run()