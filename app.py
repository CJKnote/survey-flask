from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)


app.config['SECRET_KEY'] = "codecodecode"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

survey = satisfaction_survey
responses = []

@app.route('/')
def start_page():
    """create the start page for the survey"""
    return render_template('start.html', survey=survey)

@app.route('/questions/<int:num>')
def question_page(num):
    """shows question passed in"""

    #prevent users from skipping questions/going to questions that do not exist
    if(num!=len(responses)):
        flash(f"Invalid question, redirecting to next question in the survey.")
        return redirect(f'/questions/{len(responses)}')
    
    elif(num==len(survey.questions)):
        return redirect('/finish')

    else:
        question=survey.questions[num]
        return render_template("questions.html", q_num=num, question=question)

@app.route('/answer', methods=["POST"])
def store_answer():
    """store answer into the response memory"""
    user_answer = request.form['ans']

    responses.append(user_answer)

    #check if we still have questions to answer
    if(len(responses) == len(survey.questions)):
        return redirect('/finish')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/finish')
def finish_page():
    """display the finish page"""
    return render_template("/finish.html")