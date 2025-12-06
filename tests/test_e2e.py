import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

@pytest.fixture(scope="module")
def driver():
    """Setup du driver Chrome pour Selenium."""
    # Installe le driver Chrome automatiquement
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10) # Attente max de 10s si un élément n'est pas là
    yield driver
    driver.quit()

def test_e2e_login(driver):
    """E2E: Connexion via l'interface."""
    # L'application DOIT tourner sur ce port
    driver.get("http://127.0.0.1:5000/login")
    
    # Remplir le formulaire avec l'utilisateur qu'on vient de créer
    driver.find_element(By.NAME, "username").send_keys("selenium_user")
    driver.find_element(By.NAME, "password").send_keys("password123")
    
    # Cliquer sur le bouton Login (balise <button>)
    login_btn = driver.find_element(By.TAG_NAME, "button")
    login_btn.click()
    
    # Vérifier qu'on est redirigé (plus de "Login" dans le titre)
    time.sleep(1) 
    assert "Login" not in driver.title

def test_e2e_create_task(driver):
    """E2E: Création d'une tâche via l'UI."""
    # On suppose qu'on est resté connecté du test précédent
    driver.get("http://127.0.0.1:5000/tasks/new")
    
    driver.find_element(By.NAME, "title").send_keys("Tache Selenium")
    driver.find_element(By.NAME, "description").send_keys("Automated by Robot")
    
    # Pour la date, le format dépend parfois de la langue du navigateur
    # On envoie une date simple : jj-mm-aaaa ou aaaa-mm-jj
    driver.find_element(By.NAME, "due_date").send_keys("01-01-2025")
    
    # Soumettre
    driver.find_element(By.TAG_NAME, "button").click()
    
    # Vérifier que la tâche apparaît sur la page d'accueil
    time.sleep(1)
    assert "Tache Selenium" in driver.page_source