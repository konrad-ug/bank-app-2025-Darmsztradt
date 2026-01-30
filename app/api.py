from flask import Flask, request, jsonify
from src.accounts_registry import AccountsRegistry
from src.account import PersonalAccount

app = Flask(__name__)
registry = AccountsRegistry()


@app.route("/api/accounts", methods=['POST'])
def create_account():
    data = request.get_json()
    
    if registry.find_by_pesel(data["pesel"]) is not None:
        return jsonify({"error": "Account with this PESEL already exists"}), 409
    
    account = PersonalAccount(data["name"], data["surname"], data["pesel"])
    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201


@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    accounts_data = [
        {"name": acc.first_name, "surname": acc.last_name, "pesel": acc.pesel, "balance": acc.balance}
        for acc in accounts
    ]
    return jsonify(accounts_data), 200


@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    count = registry.get_count()
    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = registry.find_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    return jsonify({
        "name": account.first_name,
        "surname": account.last_name,
        "pesel": account.pesel,
        "balance": account.balance
    }), 200


@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    account = registry.find_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    if "name" in data:
        account.first_name = data["name"]
    if "surname" in data:
        account.last_name = data["surname"]
    
    return jsonify({"message": "Account updated"}), 200


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    account = registry.find_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    registry.accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/accounts/<pesel>/transfer", methods=['POST'])
def transfer(pesel):
    account = registry.find_by_pesel(pesel)
    if account is None:
        return jsonify({"error": "Account not found"}), 404
    
    data = request.get_json()
    amount = data.get("amount")
    transfer_type = data.get("type")
    
    if transfer_type == "incoming":
        account.balance += amount
        account.history.append(amount)
        return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
    
    elif transfer_type == "outgoing":
        if account.balance >= amount:
            account.balance -= amount
            account.history.append(-amount)
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
            return jsonify({"error": "Insufficient funds"}), 422
    
    elif transfer_type == "express":
        if account.balance >= amount:
            account.balance -= amount
            account.history.append(-amount)
            account.balance -= account.express_transfer_fee
            account.history.append(-account.express_transfer_fee)
            return jsonify({"message": "Zlecenie przyjęto do realizacji"}), 200
        else:
            return jsonify({"error": "Insufficient funds"}), 422
    
    else:
        return jsonify({"error": "Unknown transfer type"}), 400
