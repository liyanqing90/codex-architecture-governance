def reserve(connection, account_id: str, amount: int) -> None:
    current = connection.execute(
        "SELECT balance FROM accounts WHERE id = ?",
        (account_id,),
    ).fetchone()[0]
    connection.execute(
        "UPDATE accounts SET balance = ? WHERE id = ?",
        (current - amount, account_id),
    )
