from app import accounts


def apply_refund(account_store, account_id: str, amount: int) -> None:
    accounts.credit(account_store, account_id, amount)
