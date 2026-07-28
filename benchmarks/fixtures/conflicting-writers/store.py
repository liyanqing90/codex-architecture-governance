def api_credit(connection, account_id: str, amount: int) -> None:
    balance = connection.read_balance(account_id)
    connection.write_balance(account_id, balance + amount)


def worker_debit(connection, account_id: str, amount: int) -> None:
    balance = connection.read_balance(account_id)
    connection.write_balance(account_id, balance - amount)
