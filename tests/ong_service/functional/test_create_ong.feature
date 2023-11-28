Feature: ONG

    Scenario: Creating a ONG
        Given I have all the required data
        And ONG is not registered

        When I register the ONG

        Then The ONG should be registered
    
    Scenario: Creating a ONG with not all required data
        Given I do not have all the required data

        When I register the ONG with invalid data

        Then I should see the error message