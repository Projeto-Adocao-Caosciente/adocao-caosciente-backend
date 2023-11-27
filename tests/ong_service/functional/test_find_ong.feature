Feature: ONG
    As a ONG I want to be able to register, update and find my ONG

    Scenario: Finding a ONG
        Given I have all the required data
        And ONG is registered

        When I search for the ONG

        Then The ONG should be found
