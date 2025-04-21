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

    },
    {
        'descriptor_type' : 'images',
        'dismissals' : [
        'run out',
        'bowled',
        'caught'
        ],
        'explanations' : [
            'The batsman is out run out if the fielder hits the stumps with the ball before the batsman reaches the crease.',
            'The batsman is out bowled if the ball hits the stumps and dislodges the bails.',
            'The batsman is out caught if the fielder catches the ball before it hits the ground.'
        ],
        'descriptors' : [
            'static/gifs/bowled.gif',
            'static/gifs/caught.gif',
            'static/gifs/runout.gif'
        ],
        'correct_order' : [
            'bowled',
            'caught',
            'run out'
        ]

    }
    
]

cricket_overview = {
        1: {
            "image": "static/images/wicket.JPG",
            "hotspots": [
                {"top": "52%", "left": "32%", "label": "Stumps"},
                {"top": "37%", "left": "33%", "label": "Bails"},
                {"top": "51%", "left": "63%", "label": "Pitch"},
                {"top": "62%", "left": "66%", "label": "Crease line"},
                {"top": "17%", "left": "65%", "label": "Infield Boundary"}
            ],
            "description": [
                "🏏 Cricket is played between 2 teams, each with 11 players",
                "🏏 It is played on an oval-shaped field. In the center, there is a rectangular strip called the pitch.",
                "🏏 At both ends of the pitch are wickets made of 3 wooden stumps and 2 small bails on top."
            ]
        },
        2: {
            "image": "static/images/field.JPG",
            "hotspots": [
                {"top": "65%", "left": "28%", "label": "Batsman (Striker)"},
                {"top": "58%", "left": "57%", "label": "Batsman (Non-striker)"},
                {"top": "52%", "left": "72%", "label": "Bowler"},
                {"top": "35%", "left": "82%", "label": "Umpire"},
                {"top": "40%", "left": "23%", "label": "Fielder"}
            ],
            "description": [
                "🏏 Batting team has two batters on the field at a time, standing at opposite ends of the pitch.",
                "🥎 The bowler bowls the ball from one end of the pitch to the batter standing at the other end.",
                "🏏 The batter tries to protect the stumps and score runs."
            ]
        },
        3: {
            "image": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGFsMnZuMHcwdTR3dGRka3o0NmdzODNydnhkYWYyaGJuZ3M4NXphcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kDXtscxqmTgm9XIWXk/giphy.gif",
            "description": [
                "Each team takes turns to bat and bowl/field. The bowler delivers the ball to the batter, who tries to hit it with a bat. The batter stands in front of the stumps and tries not to let the ball hit them.",
                "🥎 Hitting the ball and running between the wickets (1 run)",
                "🥎 Hitting the ball to the boundary along the ground (4 runs)",
                "🥎 Hitting the ball over the boundary without it touching the ground (6 runs)"
            ]
        },
        4: {
            "image": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDRlY3JtcWR2OGJ6Z2pnbnd6MDd3Mmg0NjdkNDF3Mjg3OWJzcjFsdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/kEWuibK6peH2LqbFsa/giphy.gif",
            "description": [
                "Getting Out: The fielding team tries to get the batter out. This is called a dismissal.",
                "🥎 Bowled",
                "🥎 Caught",
                "🥎 Run out",
                "🥎 LBW"
            ]
        },
        5: {
            "image": "https://media.giphy.com/media/XvisXTFLX4SuCEZzew/giphy.gif?cid=ecf05e47exw3wat42s3nb5l691srzfubxit1lng765t19x3n&ep=v1_gifs_search&rid=giphy.gif&ct=g",
            "description": [
                "When the batting team finishes their innings (either all players are out or all overs are completed), the teams switch roles.",
                "🏏 What is an over? An over consists of 6 balls bowled by one bowler. The number of overs in a match depends on the format ex. T20 has 20 overs per team.",
                "🏏 The team that scores the most runs in their innings wins the match."
            ]
        }
    }

@app.route('/')
def home():
    return render_template('homepage.html')  


@app.route('/quiz')
def quiz(quiz=quizzes[1]):
    print(quiz)
    return render_template('quiz.html', content=quiz) 


@app.route('/overview')
def overview():
    return render_template('overview.html', slides=cricket_overview)


@app.route('/dismissals')
def dismissals():
    return render_template('dismissals.html')


if __name__ == '__main__':
   app.run(debug = True, port=5001)


