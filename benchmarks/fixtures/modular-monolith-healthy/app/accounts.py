def credit(account_store, account_id: str, amount: int) -> None:
    with account_store.transaction():
        account_store.credit(account_id, amount)


def balance(account_store, account_id: str) -> int:
    return account_store.balance(account_id)
