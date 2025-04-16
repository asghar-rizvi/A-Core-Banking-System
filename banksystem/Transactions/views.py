from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from Accounts.models import Account
from .models import Transaction
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from decimal import Decimal

@method_decorator(csrf_exempt, name='dispatch')
class TransactionProcess(View):
    @transaction.atomic 
    def post(self, request):
        try:
            data = json.loads(request.body)
            sender = Account.objects.get(user=request.user)
            receiver_acc_no = data['receiver_account']
            amount = Decimal(str(data['amount']))

            if sender.account_number == receiver_acc_no:
                return JsonResponse({"error": "Cannot send to your own account"}, status=400)

            try:
                receiver = Account.objects.get(account_number=receiver_acc_no)
            except Account.DoesNotExist:
                return JsonResponse({"error": "Receiver account does not exist"}, status=404)

            if sender.balance < amount:
                return JsonResponse({"error": "Insufficient balance"}, status=400)
            
            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()

            transaction = Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
                status='SUCCESS',
                remarks=data.get('remarks', '')
            )

            return JsonResponse({
                "message": "Transfer successful",
                "transaction_id": transaction.id,
                "amount": transaction.amount,
                "timestamp": transaction.timestamp,
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class TransactionHistoryView(View):
    def get(self, request):
        try:
            account = Account.objects.get(user=request.user)
            transactions = Transaction.objects.filter(
                sender=account
            ) | Transaction.objects.filter(receiver=account)

            transactions = transactions.order_by('-timestamp')

            data = [{
                "id": tx.id,
                "type": "Sent" if tx.sender == account else "Received",
                "to_or_from": tx.receiver.account_number if tx.sender == account else tx.sender.account_number,
                "amount": float(tx.amount),
                "status": tx.status,
                "timestamp": tx.timestamp,
                "remarks": tx.remarks
            } for tx in transactions]

            return JsonResponse({"transactions": data})
        except Account.DoesNotExist:
            return JsonResponse({"error": "No account found for this user"}, status=404)
