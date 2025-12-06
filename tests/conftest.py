import pytest
import os
from app import create_app
from extensions import db as _db

@pytest.fixture(scope="module")
def app():
    """Crée une instance de l'app configurée pour les tests (Base de données en mémoire)."""
    # 1. On force la variable d'env à utiliser SQLite AVANT de créer l'app
    # Cela empêche l'app de tenter une connexion à Postgres au démarrage
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    
    app = create_app()
    
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret"
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def db(app):
    return _db