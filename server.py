from flask import Flask
from flask import render_template
from flask import Response, request, jsonify
import itertools
import re
app = Flask(__name__)

quizzes = [
    {
        'descriptor_type' : 'text',
        'dismissals' : [
        'LBW',
        'hit wicket',
        'timed out'
        ],
        'explanations' : [
            'The batsman is out LBW if the ball hits his leg and would have gone on to hit the stumps.',
            'The batsman is out timed out if he does not arrive at the crease within 3 minutes of the previous batsman being dismissed.',
            'The batsman is out hit wicket if he knocks the stumps off while attempting to hit the ball.'
        ],
        'descriptors' : [
            'Batsman took more than 3 minutes to come out to bat',
            'Batsman blocks the ball from hitting the stumps with their leg',
            'Batsman while attempting to hit the ball, hits the wicket and knocks the stumps off'
        ],
        'correct_order' : [
            'timed out',
            'LBW',
            'hit wicket'
        ]

    }
    
]


@app.route('/')
def home():
    return render_template('homepage.html')  

@app.route('/quiz')
def quiz(quiz=quizzes[0]):
    print(quiz)
    return render_template('quiz.html', content=quiz) 


if __name__ == '__main__':
   app.run(debug = True, port=5001)


