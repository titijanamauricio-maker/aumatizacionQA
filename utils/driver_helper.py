"""Ayudante para crear el WebDriver de Selenium."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://127.0.0.1:8001"


def crear_driver(navegador="chrome", headless=True):
    """Crea y devuelve el WebDriver del navegador solicitado.

    ``headless=True`` (por defecto) ejecuta el navegador en segundo plano
    (sin mostrarse). ``headless=False`` abre el navegador visible, para
    poder ver lo que está haciendo la automatización.
    """
    if navegador == "firefox":
        return webdriver.Firefox()
    opciones = Options()
    opciones.add_argument("--no-sandbox")
    opciones.add_argument("--disable-dev-shm-usage")
    if headless:
        opciones.add_argument("--headless=new")
    return webdriver.Chrome(options=opciones)
