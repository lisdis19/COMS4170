from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "volleyball_secret_key_2026"

# Add enumerate to Jinja2 globals
app.jinja_env.globals.update(enumerate=enumerate)

# Load content data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "data", "content.json")) as f:
    CONTENT = json.load(f)

LESSONS = CONTENT["lessons"]
QUIZ = CONTENT["quiz"]

with open(os.path.join(BASE_DIR, "data", "challenges.json")) as f:
    CHALLENGES = json.load(f)["challenges"]

# ---------- Simple in-memory user log (one user at a time) ----------
user_log = {
    "session_start": None,
    "lesson_visits": {},   # lesson_id -> {"timestamp": ..., "selection": ...}
}


def reset_log():
    user_log["session_start"] = datetime.now().isoformat()
    user_log["lesson_visits"] = {}


# ------------------------------------------------------------------ #
#  HOME
# ------------------------------------------------------------------ #
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/start")
def start():
    reset_log()
    session["started"] = True
    return redirect(url_for("learn", lesson_num=1))


# ------------------------------------------------------------------ #
#  LEARNING
# ------------------------------------------------------------------ #
@app.route("/learn/<int:lesson_num>", methods=["GET", "POST"])
def learn(lesson_num):
    if not session.get("started"):
        return redirect(url_for("home"))

    lesson = next((l for l in LESSONS if l["id"] == lesson_num), None)
    if lesson is None:
        return redirect(url_for("play_intro"))

    if request.method == "POST":
        selection = request.form.get("selection", "")
        user_log["lesson_visits"][str(lesson_num)] = {
            "timestamp": datetime.now().isoformat(),
            "selection": selection,
        }
        next_num = lesson_num + 1
        if next_num > len(LESSONS):
            return redirect(url_for("play_intro"))
        return redirect(url_for("learn", lesson_num=next_num))

    # GET - record page visit time
    if str(lesson_num) not in user_log["lesson_visits"]:
        user_log["lesson_visits"][str(lesson_num)] = {
            "timestamp": datetime.now().isoformat(),
            "selection": None,
        }

    total = len(LESSONS)
    return render_template(
        "learn.html",
        lesson=lesson,
        lesson_num=lesson_num,
        total=total,
        progress=int((lesson_num / total) * 100),
    )


# ------------------------------------------------------------------ #
#  BUILD-A-PLAY
# ------------------------------------------------------------------ #
@app.route("/play")
def play_intro():
    if not session.get("started"):
        return redirect(url_for("home"))
    return render_template("play_intro.html", total=len(CHALLENGES))


@app.route("/play/<int:challenge_num>")
def play_challenge(challenge_num):
    if not session.get("started"):
        return redirect(url_for("home"))
    challenge = next((c for c in CHALLENGES if c["id"] == challenge_num), None)
    if challenge is None:
        return redirect(url_for("play_result"))
    total = len(CHALLENGES)
    return render_template(
        "play.html",
        challenge=challenge,
        challenge_num=challenge_num,
        total=total,
        challenges_json=json.dumps(challenge),
    )


@app.route("/api/play/submit", methods=["POST"])
def play_submit():
    data = request.get_json()
    challenge_num = data.get("challenge_num")
    placements = data.get("placements", {})

    challenge = next((c for c in CHALLENGES if c["id"] == challenge_num), None)
    if not challenge:
        return jsonify({"error": "not found"}), 404

    correct_count = 0
    zone_results = {}
    for zone in challenge["zones"]:
        placed = placements.get(zone["id"])
        correct = placed in zone["accepts"]
        if correct:
            correct_count += 1
        zone_results[zone["id"]] = {"placed": placed, "correct": correct, "expected": zone["accepts"]}

    all_correct = correct_count == len(challenge["zones"])

    if "play_attempts" not in user_log:
        user_log["play_attempts"] = {}
    user_log["play_attempts"][str(challenge_num)] = {
        "timestamp": datetime.now().isoformat(),
        "placements": placements,
        "correct_count": correct_count,
        "total_zones": len(challenge["zones"]),
        "all_correct": all_correct,
    }

    if all_correct:
        session[f"play_{challenge_num}_done"] = True

    return jsonify({
        "correct_count": correct_count,
        "total": len(challenge["zones"]),
        "all_correct": all_correct,
        "zone_results": zone_results,
        "success_message": challenge["success_message"] if all_correct else None,
        "learn_tip": challenge["learn_tip"],
    })


@app.route("/play/result")
def play_result():
    if not session.get("started"):
        return redirect(url_for("home"))
    completed = sum(1 for c in CHALLENGES if session.get(f"play_{c['id']}_done"))
    session["started"] = False
    return render_template("play_result.html", completed=completed, total=len(CHALLENGES))


# ------------------------------------------------------------------ #
#  API log (for TA demo)
# ------------------------------------------------------------------ #
@app.route("/api/log")
def api_log():
    return jsonify(user_log)


if __name__ == "__main__":
    app.run(debug=True)