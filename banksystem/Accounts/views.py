import random
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from banksystem.Banks.models import Bank, Branch
from .models import Account
import json
from django.views.decorators.csrf import csrf_exempt



def generate_unique_account_number(bank):
    while True:
        # Generate a 10-digit number
        acc_number = str(random.randint(10**9, 10**10 - 1))
        exists = Account.objects.filter(account_number=acc_number, branch__bank=bank).exists()
        if not exists:
            return acc_number
        
@method_decorator(csrf_exempt, name='dispatch')
class AccountCreateView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            bank = Bank.objects.get(id=data['bank_id'])
            branch_code = data['branch_code']

            branch = Branch.objects.get(bank=bank, branch_code=branch_code)
            acccount = generate_unique_account_number(bank)
            new_account = Account.objects.create(
                account_number=acccount,
                user=request.user,
                branch=branch,
                balance=data['balance'],
                account_type=data['account_type'],
            )

            return JsonResponse({
                "message": "Account created",
                "account_number": new_account.account_number
            })

        except Branch.DoesNotExist:
            return JsonResponse({"error": "Branch not found for this bank."}, status=404)
        except Bank.DoesNotExist:
            return JsonResponse({"error": "Bank not found."}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(login_required, name='dispatch')
class AccountListView(View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)

        data = [{
            "account_number": acc.account_number,
            "branch_code": acc.branch.branch_code,
            "branch_address": acc.branch.address,
            "bank": acc.branch.bank.name,
            "balance": float(acc.balance),
            "type": acc.account_type,
            "created_at": acc.date_created,
        } for acc in accounts]

        return JsonResponse({"accounts": data})


class AccountDetailView(View):
    def get(self, request):
        try:
            acc = Account.objects.filter(user=request.user).first()

            if not acc:
                return JsonResponse({"error": "No accounts found"}, status=404)

            data = {
                "account_number": acc.account_number,
                "branch_code": acc.branch.branch_code,
                "branch_address": acc.branch.address,
                "bank": acc.branch.bank.name,
                "balance": float(acc.balance),
                "type": acc.account_type,
                "created_at": acc.date_created,
            }

            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
