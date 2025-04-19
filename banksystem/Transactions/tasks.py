from celery import shared_task
from decimal import Decimal
from .models import Transaction, Account

@shared_task
def perform_transaction(sender, receiver, amount, remarks=''):
    try:
        if sender.balance < amount:
            return {'status': 'FAILED', 'reason': 'Insufficient funds'}

        if sender.account_number == receiver.account_number:
            return {'status': 'FAILED', 'reason': 'Cannot transfer to same account'}

        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        txn = Transaction.objects.create(
            sender=sender,
            receiver=receiver,
            amount=amount,
            status='SUCCESS',
            remarks=remarks
        )
        return {
            'status': 'SUCCESS',
            'transaction_id': txn.id,
            'amount': str(txn.amount)
        }

    except Exception as e:
        return {'status': 'FAILED', 'reason': str(e)}
