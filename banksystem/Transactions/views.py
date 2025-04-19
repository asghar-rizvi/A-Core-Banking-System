from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from Accounts.models import Account
from .models import Transaction
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from decimal import Decimal
from django.core.cache import cache

@method_decorator(csrf_exempt, name='dispatch')
class TransactionProcess(View):
    @transaction.atomic 
    def post(self, request):
        try:
            data = json.loads(request.body)
            sender = Account.objects.get(user=request.user)
            receiver_acc_no = data['receiver_account']
            amount = Decimal(str(data['amount']))
            remarks = data.get('remarks', '')
            
            if sender.account_number == receiver_acc_no:
                return JsonResponse({"error": "Cannot send to your own account"}, status=400)

            try:
                receiver = Account.objects.get(account_number=receiver_acc_no)
            except Account.DoesNotExist:
                return JsonResponse({"error": "Receiver account does not exist"}, status=404)

            from .tasks import perform_transaction
            result = perform_transaction.delay(
                sender = sender,
                receiver=receiver,
                amount=amount,
                remarks=remarks
            )

            return JsonResponse({
                "message": "Transaction initiated.",
                "task_id": result.id
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


class TransactionHistoryView(View):
    def get(self, request):
        try:
            user = request.user
            cache_key = f"txn_history_user_{user.id}"
            data = cache.get(cache_key)
            
            if not data:
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

                cache.set(cache_key, data, timeout=300)
                
            return JsonResponse({"transactions": data})
        except Account.DoesNotExist:
            return JsonResponse({"error": "No account found for this user"}, status=404)
