from backend.models.models import TransactionRow
from typing import List, Tuple


def total_amount(transactions: List[TransactionRow]) -> float:
    return sum(transaction.amount for transaction in transactions)


def covers_levy(balance_amount: float, withdrawal_amount: float) -> Tuple[float, float]:
    if balance_amount == 0 or withdrawal_amount == 0:
        return 0.0, 0.0

    coverage_rate = min(balance_amount / withdrawal_amount, 1) * 100
    rest = (
        balance_amount - withdrawal_amount if balance_amount >= withdrawal_amount else 0
    )

    return round(coverage_rate, 2), rest
