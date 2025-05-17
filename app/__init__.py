from flask import Flask
from config import Config
from app.extensions import db, bcrypt, login_manager
import threading
from app.telegram.bot import run_bot
from app.routes.repeating import repeating_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.projects import projects_bp
    from app.routes.tasks import tasks_bp
    from app.routes.documents import documents_bp
    from app.routes.users import users_bp
    from app.routes.home import home_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(repeating_bp)
    app.register_blueprint(home_bp)


    threading.Thread(target=run_bot, daemon=True).start()

    return app
