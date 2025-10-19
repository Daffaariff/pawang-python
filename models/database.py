# models/database.py
import sqlite3
from flask import g
from config import settings
import srsly

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(settings.DATABASE_URL)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            nickname TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL,
            score INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL
        );
        """)
        db.commit()
    app.teardown_appcontext(close_db)

def seed_quiz_data():
    """Insert quiz data from JSONL file if the table is empty."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM quiz")
    count = cursor.fetchone()[0]

    if count == 0:
        quiz_questions = list(srsly.read_jsonl(settings.QUIZ_SAMPLE_PATH))

        if not quiz_questions:
            print("❌ No quiz questions loaded. Using fallback questions.")
            quiz_questions = [
                {
                    "question": "Lengkapi kode berikut:\n\nfrom sklearn import ______\niris = ______.load_iris()",
                    "option_a": "datasets, datasets",
                    "option_b": "model, model",
                    "option_c": "data, data",
                    "option_d": "learning, learning",
                    "correct_option": "A"
                }
            ]

        for question in quiz_questions:
            # Ensure code questions have proper newlines for display
            if any(keyword in question["question"].lower() for keyword in ["lengkapi", "kode", "from ", "import ", "def ", "class "]):
                # Format with proper indentation for code display
                question["question"] = question["question"].replace("\\n", "\n")

            cursor.execute(
                "INSERT INTO quiz (question, option_a, option_b, option_c, option_d, correct_option) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    question["question"],
                    question["option_a"],
                    question["option_b"],
                    question["option_c"],
                    question["option_d"],
                    question["correct_option"]
                )
            )

        db.commit()
        print(f"✅ Seeded {len(quiz_questions)} quiz questions successfully!")
    else:
        print(f"✅ Quiz table already has {count} questions. No seeding needed.")

def clear_quiz_data():
    """Clear all quiz data from the database."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM quiz")
        db.commit()
        print("✅ All quiz questions deleted successfully!")
        return True
    except Exception as e:
        print(f"❌ Error deleting quiz data: {e}")
        db.rollback()
        return False

def reset_quiz_sequence():
    """Reset the auto-increment sequence for quiz IDs."""
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='quiz'")
        db.commit()
        print("✅ Quiz sequence reset successfully!")
        return True
    except Exception as e:
        print(f"❌ Error resetting quiz sequence: {e}")
        return False