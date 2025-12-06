import os
from datetime import date, timedelta
from models import User, Task
from app import _build_postgres_uri

def test_user_password_hashing():
    """Test: User.set_password et check_password fonctionnent."""
    u = User(username="testuser")
    u.set_password("mypassword")
    
    assert u.password_hash != "mypassword"
    assert u.check_password("mypassword") is True
    assert u.check_password("wrongpass") is False

def test_task_is_overdue_logic():
    """Test: La logique de retard (is_overdue)."""
    future_task = Task(due_date=date.today() + timedelta(days=1), is_completed=False)
    assert future_task.is_overdue() is False

    past_task = Task(due_date=date.today() - timedelta(days=1), is_completed=False)
    assert past_task.is_overdue() is True

    completed_task = Task(due_date=date.today() - timedelta(days=1), is_completed=True)
    assert completed_task.is_overdue() is False

def test_build_postgres_uri_env_parsing(monkeypatch):
    """Test: URI Postgres via variables d'env (avec nettoyage automatique)."""
    # monkeypatch modifie l'environnement SEULEMENT pour ce test
    monkeypatch.setenv("POSTGRES_USER", "testuser")
    monkeypatch.setenv("POSTGRES_PASSWORD", "testpass")
    monkeypatch.setenv("POSTGRES_HOST", "testhost")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "testdb")
    
    # On s'assure que DATABASE_URL n'est pas défini
    monkeypatch.delenv("DATABASE_URL", raising=False)

    uri = _build_postgres_uri()
    expected = "postgresql+psycopg2://testuser:testpass@testhost:5432/testdb"
    assert uri == expected
    # À la fin de la fonction, monkeypatch remet tout comme avant automatiquement !