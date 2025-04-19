from django.http import JsonResponse
from django.views import View
from .models import Bank, Branch
from django.core.cache import cache

class BankListView(View):
    def get(self, request):
        key = 'ALLBANKS'
        data = cache.get(key)
        if not data:
            banks = Bank.objects.all()
            data = [{"code": bank.code, "name": bank.name} for bank in banks]
            cache.set(key,data, timeout=200)
        return JsonResponse(data, safe=False)

class BranchListView(View):
    def get(self, request, bank_code):
        key = f'bank_{bank_code}'
        data = cache.get(key)
        if not data:    
            branches = Branch.objects.filter(bank__code=bank_code)
            data = [{
                "branch_code": branch.branch_code,
                "address": branch.address
            } for branch in branches]
            cache.set(key,data, timeout=120)
        return JsonResponse(data, safe=False)