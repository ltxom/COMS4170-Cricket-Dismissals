
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import datetime

app = Flask(__name__)

with open('data/dismissals.json') as f:
    dismissal_data = json.load(f)['dismissals']

user_logs = []  
with open("user_logs.jsonl", "w") as log_file:
    log_file.write("")

def log_user_action(page, action=None):
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "page": page,
        "action": action
    }
    user_logs.append(log_entry)
    print(f"[User Log] {log_entry}")
    with open("user_logs.jsonl", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")


# --- Overview content defined before use ---
cricket_overview = {
    1: {
        "image": "static/images/wicket.JPG",
        "hotspots": [
            {"top": "54%", "left": "32%", "label": "Stumps"},
            {"top": "38%", "left": "33%", "label": "Bails"},
            {"top": "53%", "left": "63%", "label": "Pitch"},
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
    log_user_action(page="Home", action="Page Enter")
    return render_template('homepage.html')

@app.route('/overview')
def overview():
    log_user_action(page="Overview", action="Page Enter")
    return render_template('overview.html', slides=cricket_overview)

@app.route('/dismissal')
def dismissals_main():
    # log_user_action(page="Dismissals", action="Page Enter")
    return redirect(url_for('dismissal_page', id=1))

@app.route('/dismissal/<int:id>')
def dismissal_page(id):
    if id < 1 or id > len(dismissal_data):
        return redirect(url_for('dismissals_main'))
    dismissal = dismissal_data[id - 1]
    log_user_action(page=dismissal["name"], action="Page Enter")
    return render_template('dismissal_detail.html', dismissal=dismissal, dismissals=dismissal_data, total=len(dismissal_data))

@app.route('/start-quiz')
def startQuiz():
    log_user_action(page="Start Quiz", action="Page Enter")
    return render_template('transition.html')

# --- Quiz Functionality ---
quizzes = [
    {
        'descriptor_type' : 'text',
        'dismissals' : ['LBW', 'hit wicket', 'timed out'],
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
        'correct_order' : ['timed out', 'LBW', 'hit wicket']
    },
    {
        'descriptor_type' : 'images',
        'dismissals' : ['run out', 'bowled', 'caught'],
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
        'correct_order' : ['bowled', 'caught', 'run out']
    }
]

current_quiz_index = 0
user_answers = []

@app.route('/quiz')
def quiz(quiz=quizzes[0]):
    global current_quiz_index, user_answers
    current_quiz_index = 0
    user_answers = []
    return render_template("quiz.html", content=quizzes[current_quiz_index])

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():
    global current_quiz_index, user_answers
    data = request.json
    answers = data.get("answers", [])
    user_answers.append(answers)
    if current_quiz_index < len(quizzes) - 1:
        current_quiz_index += 1
        return jsonify({"next_quiz": quizzes[current_quiz_index]})
    else:
        return jsonify({"next_quiz": None})

@app.route("/quiz-results")
def quiz_results():
    global user_answers
    total_score = 0
    max_score = 0
    for i, quiz in enumerate(quizzes):
        correct_order = quiz["correct_order"]
        user_response = user_answers[i] if i < len(user_answers) else []
        max_score += len(correct_order)
        total_score += sum(1 for j in range(len(correct_order)) if j < len(user_response) and user_response[j] == correct_order[j])
    return render_template("quiz_results.html", total_score=total_score, max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
