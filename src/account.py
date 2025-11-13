class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []

    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(amount)

    def outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.history.append(-amount)

