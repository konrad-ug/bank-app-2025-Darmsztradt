Feature: Account transfers
    Scenario: User can make an incoming transfer
        Given Account registry is empty
        And I create an account using name: "john", last name: "doe", pesel: "12345678901"
        When I make an incoming transfer of "500" to account with pesel: "12345678901"
        Then Account with pesel "12345678901" has balance of "500"

    Scenario: User can make an outgoing transfer with sufficient funds
        Given Account registry is empty
        And I create an account using name: "john", last name: "doe", pesel: "12345678901"
        And I make an incoming transfer of "1000" to account with pesel: "12345678901"
        When I make an outgoing transfer of "300" from account with pesel: "12345678901"
        Then Account with pesel "12345678901" has balance of "700"

    Scenario: Outgoing transfer fails with insufficient funds
        Given Account registry is empty
        And I create an account using name: "john", last name: "doe", pesel: "12345678901"
        And I make an incoming transfer of "100" to account with pesel: "12345678901"
        When I try to make an outgoing transfer of "500" from account with pesel: "12345678901"
        Then The transfer should fail with insufficient funds
        And Account with pesel "12345678901" has balance of "100"

    Scenario: User can make an express transfer
        Given Account registry is empty
        And I create an account using name: "john", last name: "doe", pesel: "12345678901"
        And I make an incoming transfer of "1000" to account with pesel: "12345678901"
        When I make an express transfer of "500" from account with pesel: "12345678901"
        Then Account with pesel "12345678901" has balance of "499"

    Scenario: Multiple transfers update balance correctly
        Given Account registry is empty
        And I create an account using name: "john", last name: "doe", pesel: "12345678901"
        When I make an incoming transfer of "1000" to account with pesel: "12345678901"
        And I make an outgoing transfer of "200" from account with pesel: "12345678901"
        And I make an incoming transfer of "300" to account with pesel: "12345678901"
        Then Account with pesel "12345678901" has balance of "1100"
