Feature: ONG
    As a ONG I want to be able to register my ONG

    Scenario: Creating a ONG
        Given I have all the required data
        And ONG is not registered

        When I register the ONG

        Then The ONG should be registered