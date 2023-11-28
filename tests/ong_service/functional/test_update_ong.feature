Feature: ONG

    Scenario: Updating a ONG
        Given I have all the required data to update
        And ONG is registered

        When I update the ONG

        Then All the data should be updated

    Scenario: Updating a ONG that does not exist
        Given ONG is not registered

        When I update the ONG that does not exist

        Then I should receive an error message
    
    Scenario: Updating a ONG with invalid data
        Given I have all the required data to update
        And ONG is registered

        When I update the ONG with invalid data

        Then I should receive an error message

    Scenario: Try to update the password of a ONG
        Given I have all the required data to update
        And ONG is registered

        When I update the password of the ONG

        Then I should receive an error message
