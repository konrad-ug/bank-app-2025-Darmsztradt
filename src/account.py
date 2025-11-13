class Account:
    def __init__(self):
        self.balance = 0.0
        self.historia = []

    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount
            self.historia.append(amount)

    def outgoing_transfer(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            self.historia.append(-amount)

