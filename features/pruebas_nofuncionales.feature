Feature: Pruebas no funcionales del sistema

  Scenario: Ver los tipos de pruebas no funcionales
    Given I open the system page
    And I am in the Pruebas module
    When I click "Pruebas no funcionales"
    Then the following test types appear: Recuperación
