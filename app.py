from flask import Flask, render_template, session
from config import settings
from models.database import init_db, seed_quiz_data, get_db
from routes.auth_routes import auth_bp
from routes.quiz_routes import quiz_bp
from routes.weather_routes import weather_bp
from utils.weather_api import get_weather_forecast

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DATABASE_URL"] = settings.DATABASE_URL
    app.config["DEBUG"] = settings.DEBUG

    # Initialize DB and seed data
    init_db(app)
    with app.app_context():
        seed_quiz_data()

    # Register routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(weather_bp)

    @app.route("/")
    def home():
        user_city = "Jakarta"  # default city
        weather = None

        if "user_id" in session:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT city FROM users WHERE id = ?", (session["user_id"],))
            result = cursor.fetchone()
            if result and result["city"]:
                user_city = result["city"]

        weather = get_weather_forecast(user_city)
        return render_template("index.html", weather=weather)


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=settings.DEBUG)
