"""Definiciones de pasos Gherkin para las pruebas funcionales y no funcionales."""
from behave import given, then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.driver_helper import BASE_URL


def _esperar_elemento(context, xpath, timeout=25):
    return WebDriverWait(context.driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


@given('I open the system page')
def step_abrir_sistema(context):
    context.driver.get(BASE_URL)
    _esperar_elemento(
        context, "//aside//p[normalize-space() = 'Pruebas QA']"
    )


@given('I am in the {modulo} module')
def step_estar_en_modulo(context, modulo):
    context.driver.get(BASE_URL)
    _esperar_elemento(
        context, "//aside//p[normalize-space() = 'Pruebas QA']"
    )
    _esperar_elemento(
        context, f"//aside//button[normalize-space() = '{modulo}']"
    ).click()
    _esperar_elemento(
        context, f"//main//h1[normalize-space() = '{modulo}']"
    )


@when('I click "{boton}"')
def step_hacer_clic_boton(context, boton):
    _esperar_elemento(
        context, f"//main//button[contains(normalize-space(.), '{boton}')]"
    ).click()


@then('the following buttons appear: {lista}')
def step_aparecen_botones(context, lista):
    for nombre in (n.strip() for n in lista.split(',') if n.strip()):
        _esperar_elemento(
            context,
            f"//main//button[contains(normalize-space(.), '{nombre}')]",
        )


@then('the following test types appear: {lista}')
def step_aparecen_tipos(context, lista):
    for tipo in (t.strip() for t in lista.split(',') if t.strip()):
        _esperar_elemento(
            context, f"//main//li[normalize-space() = '{tipo}']"
        )


@then('the page loads correctly')
def step_pagina_carga(context):
    _esperar_elemento(context, "//main//h1[normalize-space() = 'Pruebas']")
