Feature: ONG
    As a user, I want to create a ONG, So I can register my ONG

    Scenario: Creating a ONG
        Given I have all the required data
        And ONG is not registered

        When I register the ONG

        Then I should be able to login with the ONG

    Scenario: Finding a ONG
        Given I have all the required data
        And ONG is registered

        When I search for the ONG

        Then I should be able to find the ONG

    Scenario: Updating a ONG
        Given I have all the required data to update
        And ONG is registered

        When I update the ONG

        Then All the data should be updated