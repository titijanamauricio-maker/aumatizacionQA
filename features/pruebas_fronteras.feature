Feature: Pruebas de fronteras en el módulo Pruebas
  El módulo Pruebas responde a los módulos definidos en la app.

  Scenario Outline: Módulos válidos de navegación
    Given I am in the <modulo> module

  Scenarios:
    | modulo    |
    | Pruebas   |
    | Historial |
    | Reportes  |
