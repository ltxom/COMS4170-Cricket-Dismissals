from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import datetime
from collections import defaultdict

app = Flask(__name__)

# --- Overview content defined early so it's available for route use ---
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
            "Cricket is played between 2 teams, each with 11 players.",
            "It is played on an oval-shaped field. In the center, there is a rectangular strip called the pitch.",
            "At both ends of the pitch are wickets made of 3 wooden stumps and 2 small bails on top."
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
            "The batting team has two batters on the field at a time, standing at opposite ends of the pitch.",
            "The bowler bowls the ball from one end of the pitch to the batter standing at the other end.",
            "The batter tries to protect the stumps and score runs."
        ]
    },
    3: {
        "image": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGFsMnZuMHcwdTR3dGRka3o0NmdzODNydnhkYWYyaGJuZ3M4NXphcSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kDXtscxqmTgm9XIWXk/giphy.gif",
        "description": [
            "Each team takes turns to bat and bowl/field.",
            "The bowler delivers the ball to the batter, who tries to hit it with a bat.",
            "The batter stands in front of the stumps and tries not to let the ball hit them.",
            "Ways to score: run between the wickets (1 run), hit boundary on ground (4), hit over boundary (6)."
        ]
    },
    4: {
        "image": "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDRlY3JtcWR2OGJ6Z2pnbnd6MDd3Mmg0NjdkNDF3Mjg3OWJzcjFsdyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/kEWuibK6peH2LqbFsa/giphy.gif",
        "description": [
            "Getting Out: The fielding team tries to get the batter out. This is called a dismissal.",
            "Common dismissals include: Bowled, Caught, Run out, LBW."
        ]
    },
    5: {
        "image": "https://media.giphy.com/media/XvisXTFLX4SuCEZzew/giphy.gif?cid=ecf05e47exw3wat42s3nb5l691srzfubxit1lng765t19x3n&ep=v1_gifs_search&rid=giphy.gif&ct=g",
        "description": [
            "When the batting team finishes their innings (either all players are out or all overs are completed), the teams switch roles.",
            "An over consists of 6 balls bowled by one bowler.",
            "The team with the most runs after both innings wins the match."
        ]
    }
}

with open('data/dismissals.json', encoding='utf-8', errors='replace') as f:
    dismissal_data = json.load(f)['dismissals']

# Generate display names like "LBW (1 of 2)"
name_counts = defaultdict(int)
for d in dismissal_data:
    name_counts[d['name']] += 1

name_tracker = defaultdict(int)
for d in dismissal_data:
    name = d['name']
    if name_counts[name] > 1:
        name_tracker[name] += 1
        total = name_counts[name]
        d['display_name'] = f"{name} ({name_tracker[name]} of {total})"
    else:
        d['display_name'] = name

# Map dismissal id for easy access
dismissal_by_id = {d['id']: d for d in dismissal_data}

# Custom sidebar order (matches flow)
custom_order = [
    "Bowled", "Caught", "LBW", "Run Out", "Stumped",
    "Retired Out", "Double Hit / Hit the Ball Twice", "Hit Wicket",
    "Obstructing the Field", "Timed Out"
]

unique_names = []
added = set()
for name in custom_order:
    for d in dismissal_data:
        if d['name'] == name and name not in added:
            unique_names.append({'name': name, 'id': d['id']})
            added.add(name)

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
    return redirect(url_for('dismissal_page', id=1))

@app.route('/dismissal/<int:id>')
def dismissal_page(id):
    dismissal = dismissal_by_id.get(id)
    if not dismissal:
        return "Dismissal not found", 404

    log_user_action(page=dismissal["display_name"], action="Page Enter")

    # Use custom_order to determine navigation flow
    custom_ids = [d['id'] for name in custom_order for d in dismissal_data if d['name'] == name]

    if id in custom_ids:
        idx = custom_ids.index(id)
        prev_id = custom_ids[idx - 1] if idx > 0 else None
        next_id = custom_ids[idx + 1] if idx < len(custom_ids) - 1 else None
    else:
        prev_id = next_id = None  # fallback


    return render_template(
        'dismissal_detail.html',
        dismissal=dismissal,
        dismissals=dismissal_data,
        total=len(dismissal_data),
        prev_id=prev_id,
        next_id=next_id,
        unique_names=unique_names,
        total_unique=len(unique_names)
    )


@app.route('/start-quiz')
def startQuiz():
    log_user_action(page="Start Quiz", action="Page Enter")
    return render_template('transition.html')

quizzes = [
    {
        'descriptor_type': 'text',
        'dismissals': ['stumped', 'retired', 'double hit'],
        'explanations': [
            'The batsman is out stumped if he steps out of the crease and the wicketkeeper dislodges the bails.',
            'The batsman is out retired if he leaves the field and does not return.',
            'The batsman is out double hit if he hits the ball twice.'
        ],
        'descriptors': [
            'Batsman stepped out of the crease and the wicketkeeper dislodged the bails',
            'Batsman left the field and did not return',
            'Batsman hit the ball twice'
        ],
        'correct_order': ['timed out', 'LBW', 'hit wicket']
    },
    {
        'descriptor_type': 'text',
        'dismissals': ['LBW', 'hit wicket', 'timed out'],
        'explanations': [
            'The batsman is out timed out if he does not arrive at the crease within 3 minutes of the previous batsman being dismissed.',
            'The batsman is out LBW if the ball hits his leg and would have gone on to hit the stumps.',
            'The batsman is out hit wicket if he knocks the stumps off while attempting to hit the ball.'
        ],
        'descriptors': [
            'Batsman took more than 3 minutes to come out to bat',
            'Batsman blocks the ball from hitting the stumps with their leg',
            'Batsman while attempting to hit the ball, hits the wicket and knocks the stumps off'
        ],
        'correct_order': ['timed out', 'LBW', 'hit wicket']
    },
    {
        'descriptor_type': 'images',
        'dismissals': ['run out', 'bowled', 'caught'],
        'explanations': [
            'The batsman is out bowled if the ball hits the stumps and dislodges the bails.',
            'The batsman is out caught if the fielder catches the ball before it hits the ground.',
            'The batsman is out run out if the fielder hits the stumps with the ball before the batsman reaches the crease.'
            
        ],
        'descriptors': [
            'static/gifs/bowled.gif',
            'static/gifs/caught.gif',
            'static/gifs/runout.gif'
        ],
        'correct_order': ['bowled', 'caught', 'run out']
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
    feedback = []

    for i, quiz in enumerate(quizzes):
        correct_order = quiz["correct_order"]
        user_response = user_answers[i] if i < len(user_answers) else []
        explanations = quiz["explanations"]
        descriptors = quiz["descriptors"]
        question_feedback = []

        max_score += len(correct_order)
        for j in range(len(correct_order)):
            feedback_item = {
                "descriptor": descriptors[j],
                "user_answer": user_response[j] if j < len(user_response) else None,
                "correct": user_response[j] == correct_order[j] if j < len(user_response) else False,
                "correct_answer": correct_order[j],
                "explanation": explanations[j] if j < len(explanations) else None
            }
            if feedback_item["correct"]:
                total_score += 1
            question_feedback.append(feedback_item)

        feedback.append(question_feedback)

    return render_template(
        "quiz_results.html",
        total_score=total_score,
        max_score=max_score,
        feedback=feedback
    )

if __name__ == '__main__':
    app.run(debug=True, port=5001)

