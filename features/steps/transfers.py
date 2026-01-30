from behave import *
import requests

URL = "http://localhost:5000"


@when('I make an incoming transfer of "{amount}" to account with pesel: "{pesel}"')
@step('I make an incoming transfer of "{amount}" to account with pesel: "{pesel}"')
def make_incoming_transfer(context, amount, pesel):
    json_body = {
        "amount": int(amount),
        "type": "incoming"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Incoming transfer failed: {response.json()}"


@when('I make an outgoing transfer of "{amount}" from account with pesel: "{pesel}"')
@step('I make an outgoing transfer of "{amount}" from account with pesel: "{pesel}"')
def make_outgoing_transfer(context, amount, pesel):
    json_body = {
        "amount": int(amount),
        "type": "outgoing"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Outgoing transfer failed: {response.json()}"


@when('I try to make an outgoing transfer of "{amount}" from account with pesel: "{pesel}"')
def try_outgoing_transfer(context, amount, pesel):
    json_body = {
        "amount": int(amount),
        "type": "outgoing"
    }
    context.last_response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)


@then('The transfer should fail with insufficient funds')
def transfer_should_fail(context):
    assert context.last_response.status_code == 422, f"Expected 422, got {context.last_response.status_code}"


@when('I make an express transfer of "{amount}" from account with pesel: "{pesel}"')
def make_express_transfer(context, amount, pesel):
    json_body = {
        "amount": int(amount),
        "type": "express"
    }
    response = requests.post(URL + f"/api/accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200, f"Express transfer failed: {response.json()}"


@then('Account with pesel "{pesel}" has balance of "{balance}"')
def check_balance(context, pesel, balance):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    account = response.json()
    actual_balance = account["balance"]
    expected_balance = int(balance)
    assert actual_balance == expected_balance, f"Expected balance {expected_balance}, got {actual_balance}"
