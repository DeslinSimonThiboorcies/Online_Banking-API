from flask import Flask
from bank.config import Config
from bank.extensions.db import db
from bank.extensions.jwt import jwt

def creat_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)


    from bank.route.users_route.admin_route import admin_bp
    app.register_blueprint(
        admin_bp,
        url_prefix = "/api"
    )

    from bank.route.users_route.manager_route import manager_bp
    app.register_blueprint(
        manager_bp,
        url_prefix = "/api"
    )
    
    from bank.route.users_route.customer_services_route import c_s_bp
    app.register_blueprint(
        c_s_bp,
        url_prefix = "/api"
    )

    from bank.route.users_route.employee_route import employee_bp
    app.register_blueprint(
        employee_bp,
        url_prefix = "/api"
    )

    from bank.route.users_route.customer_route import customer_bp
    app.register_blueprint(
        customer_bp,
        url_prefix = "/api"
    )

    from bank.route.account_route.bankaccount_route import account_bp
    app.register_blueprint(
        account_bp,
        url_prefix = "/api"
    )
    
    return app