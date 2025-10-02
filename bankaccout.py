class Account:
    def __init__(self, balance, acc_no):
        self.balance = balance
        self.acc_no = acc_no
        self.history = []  # Store transaction history

    def methods(self):
        print("x====================================x")
        method = input("debit, credit, balance, history, end :").strip().lower()

        if method == "debit":
            amt = int(input("debit amount :"))
            if amt > self.balance:
                print("Insufficent balance")
                self.history.append(
                    f"Failed debit of {amt} (Insufficient balance)")
            else:
                self.balance -= amt
                print("Amount debited :", amt)
                print("new_balance =", self.balance)
                self.history.append(f"Debited {amt}")
            self.methods()
        elif method == "credit":
            amt = int(input("credit amount :"))
            self.balance += amt
            print("Amount credited :", amt)
            print("new_balance =", self.balance)
            self.history.append(f"Credited {amt}")
            self.methods()
        elif method == "balance":
            print("your balance is :", self.balance)
            self.methods()
        elif method == "history":
            print("Transaction history:")
            for entry in self.history:
                print(entry)
            self.methods()
        elif method == "end":
            print("Thank you, come again")
        else:
            print("Invalid option")
            self.methods()

# example
s1 = Account(100000, 14523910)
print("Account no: ", s1.acc_no)
print("Balance:", s1.balance)
s1.methods()
