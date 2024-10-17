from typing import Any, List
from backend.db.in_memory_database import InMemoryDB
from backend.logic import transactions
from backend.logic.utilities import covers_levy, total_amount
from backend.models.models import TransactionState, TransactionType

db = InMemoryDB()


def calcul_balance(user_id: int) -> float:
    completed_deposits = transactions.transactions_by_type_states(
        db, user_id, TransactionType.DEPOSIT, [TransactionState.COMPLETED]
    )
    refunds = transactions.transactions_by_type_states(
        db,
        user_id,
        TransactionType.REFUND,
        [TransactionState.COMPLETED, TransactionState.PENDING],
    )
    completed_withdrawals = transactions.transactions_by_type_states(
        db, user_id, TransactionType.SCHEDULED_WITHDRAWAL, [TransactionState.COMPLETED]
    )

    return (
        total_amount(completed_deposits)
        - total_amount(refunds)
        - total_amount(completed_withdrawals)
    )


def get_coverage_of_scheduled_withdrawals(user_id: int) -> List[Any]:
    balance = calcul_balance(user_id)

    scheduled_withdrawals = transactions.transactions_by_type_states(
        db, user_id, TransactionType.SCHEDULED_WITHDRAWAL, [TransactionState.SCHEDULED]
    )

    scheduled_withdrawals_sorted = sorted(
        scheduled_withdrawals, key=lambda transaction: transaction.date
    )

    coverage_of_scheduled_withdrawals = []

    for scheduled_withdrawal in scheduled_withdrawals_sorted:

        coverage_rate, balance = covers_levy(balance, scheduled_withdrawal.amount)

        scheduled_withdrawal_dict = scheduled_withdrawal.__dict__.copy()
        scheduled_withdrawal_dict["coverage_rate"] = coverage_rate
        coverage_of_scheduled_withdrawals.append(scheduled_withdrawal_dict)

    return coverage_of_scheduled_withdrawals
