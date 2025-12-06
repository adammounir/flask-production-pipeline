def test_register_and_login_flow(client):
    """Test: S'inscrire puis se connecter."""
    # 1. Inscription
    response = client.post("/register", data={
        "username": "integration_user",
        "password": "password123",
        "confirm": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful" in response.data

    # 2. Connexion
    response = client.post("/login", data={
        "username": "integration_user",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

def test_create_task(client):
    """Test: Créer une tâche (nécessite d'être connecté)."""
    # On doit être connecté (la session est gardée grâce au client pytest)
    # Si le test est isolé, on se reconnecte :
    client.post("/login", data={"username": "integration_user", "password": "password123"})

    response = client.post("/tasks/new", data={
        "title": "Integration Task",
        "description": "Testing creation",
        "due_date": "2025-12-31"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Task created" in response.data
    assert b"Integration Task" in response.data

def test_toggle_task(client):
    """Test: Changer le statut d'une tâche."""
    # On suppose que la tâche créée au test précédent (ID 1) existe
    client.post("/login", data={"username": "integration_user", "password": "password123"})
    
    response = client.post("/tasks/1/toggle", follow_redirects=True)
    assert response.status_code == 200
    assert b"Task status updated" in response.data