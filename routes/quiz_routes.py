# routes/quiz_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import random
from models.database import get_db

quiz_bp = Blueprint("quiz", __name__, url_prefix="/quiz")

# -------- QUIZ HOME / READY PAGE --------
@quiz_bp.route("/")
def quiz_home():
    if "user_id" not in session:
        flash("You must log in to take the quiz!", "error")
        return redirect(url_for("auth.login"))

    return render_template("quiz_ready.html")

# -------- START QUIZ --------
@quiz_bp.route("/start", methods=["POST"])
def start_quiz():
    if "user_id" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.login"))

    db = get_db()
    cursor = db.cursor()

    # Fetch all questions
    cursor.execute("SELECT * FROM quiz")
    questions = cursor.fetchall()

    # Shuffle order
    random.shuffle(questions)

    # Limit to 10 questions
    questions = questions[:10]

    # Store in session
    session["quiz_progress"] = 0
    session["quiz_score"] = 0
    session["quiz_questions"] = [dict(q) for q in questions]

    flash("Quiz started! Good luck! 🚀", "success")
    return redirect(url_for("quiz.question"))

# -------- DISPLAY QUESTIONS --------
@quiz_bp.route("/question", methods=["GET", "POST"])
def question():
    if "user_id" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.login"))

    # Check if quiz has been started
    if "quiz_questions" not in session or not session["quiz_questions"]:
        flash("Please start the quiz first!", "error")
        return redirect(url_for("quiz.quiz_home"))

    progress = session.get("quiz_progress", 0)
    questions = session.get("quiz_questions", [])

    if progress >= len(questions):
        return redirect(url_for("quiz.results"))

    current = questions[progress]

    if request.method == "POST":
        answer = request.form.get("answer")
        correct = current["correct_option"]

        if answer == correct:
            session["quiz_score"] += 1

        session["quiz_progress"] += 1

        # Check if quiz is complete after this answer
        if session["quiz_progress"] >= len(questions):
            return redirect(url_for("quiz.results"))
        else:
            return redirect(url_for("quiz.question"))

    return render_template("quiz.html", q=current, progress=progress + 1, total=len(questions))

# -------- RESULTS PAGE --------
@quiz_bp.route("/results")
def results():
    if "user_id" not in session:
        flash("Please log in first.", "error")
        return redirect(url_for("auth.login"))

    # Check if quiz has been completed
    if "quiz_score" not in session or "quiz_questions" not in session:
        flash("Please complete a quiz first!", "error")
        return redirect(url_for("quiz.quiz_home"))

    db = get_db()
    user_id = session.get("user_id")
    score = session.get("quiz_score", 0)
    total = len(session.get("quiz_questions", []))

    # Save score to user
    db.execute("UPDATE users SET score=? WHERE id=?", (score, user_id))
    db.commit()

    # Clear quiz session data
    session.pop("quiz_progress", None)
    session.pop("quiz_score", None)
    session.pop("quiz_questions", None)

    flash(f"Quiz completed! You scored {score}/{total}! 🎉", "success")
    return redirect(url_for("quiz.leaderboard"))

# -------- LEADERBOARD --------
@quiz_bp.route("/leaderboard")
def leaderboard():
    db = get_db()
    cursor = db.execute("SELECT nickname, score FROM users ORDER BY score DESC LIMIT 10")
    leaderboard = cursor.fetchall()
    return render_template("leaderboard.html", leaderboard=leaderboard)