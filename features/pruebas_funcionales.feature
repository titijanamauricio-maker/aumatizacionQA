Feature: Pruebas funcionales del sistema

  Scenario: Ver los botones de pruebas funcionales y no funcionales
    Given I open the system page
    And I am in the Pruebas module
    Then the following buttons appear: Pruebas funcionales, Pruebas no funcionales

  Scenario: Ver los tipos de pruebas funcionales
    Given I open the system page
    And I am in the Pruebas module
    When I click "Pruebas funcionales"
    Then the following test types appear: Unidad, Interfaz de usuario, Servicios Web, Regresión

  Scenario: Tipo de prueba Unidad
    Given I open the system page
    And I am in the Pruebas module
    When I click "Pruebas funcionales"
    Then the following test types appear: Unidad

  Scenario: Tipo de prueba Interfaz de usuario
    Given I open the system page
    And I am in the Pruebas module
    When I click "Pruebas funcionales"
    Then the following test types appear: Interfaz de usuario

  Scenario: Tipo de prueba Servicios Web
    Given I open the system page
    And I am in the Pruebas module
    When I click "Pruebas funcionales"
    Then the following test types appear: Servicios Web

  Scenario: Tipo de prueba Regresión
    Given I open the system page
    And I am in the Pruebas module
    When I click "Pruebas funcionales"
    Then the following test types appear: Regresión
