from django.http import JsonResponse
from django.views import View
from .models import Bank, Branch

class BankListView(View):
    def get(self, request):
        banks = Bank.objects.all()
        data = [{"code": bank.code, "name": bank.name} for bank in banks]
        return JsonResponse(data, safe=False)

class BranchListView(View):
    def get(self, request, bank_code):
        branches = Branch.objects.filter(bank__code=bank_code)
        data = [{
            "branch_code": branch.branch_code,
            "address": branch.address
        } for branch in branches]
        return JsonResponse(data, safe=False)