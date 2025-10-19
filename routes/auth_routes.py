from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# -------- REGISTER --------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    db = get_db()
    if request.method == "POST":
        username = request.form["username"].strip()
        nickname = request.form["nickname"].strip()
        password = request.form["password"]
        city = request.form["city"].strip()

        # ✅ Validate fields
        if not username or not nickname or not password or not city:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("auth.register"))

        # ✅ Check duplicates
        cursor = db.execute(
            "SELECT * FROM users WHERE username=? OR nickname=?",
            (username, nickname),
        )
        existing = cursor.fetchone()
        if existing:
            flash("Username or nickname already exists.", "error")
            return redirect(url_for("auth.register"))

        # ✅ Save new user (single insert)
        hashed = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, password, nickname, city) VALUES (?, ?, ?, ?)",
            (username, hashed, nickname, city),
        )
        db.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# -------- LOGIN --------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    db = get_db()
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        cursor = db.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["nickname"] = user["nickname"]
            flash(f"Welcome back, {user['nickname']}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")


# -------- LOGOUT --------
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))
