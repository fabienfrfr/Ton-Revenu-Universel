Feature: Simulation de revenu de base
  Scenario: Calculer le revenu de base pour un célibataire sans enfant
    Given un revenu mensuel de 2000 euros
    And un statut "celibataire"
    And 0 enfants
    When je lance la simulation
    Then le revenu de base doit être 1000 euros
    And le revenu total doit être 3000 euros
