import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banksystem.settings')  
django.setup()

from Banks.models import Bank, Branch

pakistani_banks = [
    {
        "code": "HBL001",
        "name": "Habib Bank Limited",
        "swift_code": "HABBPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "I.I Chundrigar Road, Karachi", "phone": "+922111111111"},
            {"branch_code": "002", "address": "Clifton, Karachi", "phone": "+922122222222"}
        ]
    },
    {
        "code": "UBL002",
        "name": "United Bank Limited",
        "swift_code": "UNILPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "MA Jinnah Road, Karachi", "phone": "+922133333333"},
            {"branch_code": "002", "address": "DHA Phase 5, Karachi", "phone": "+922144444444"}
        ]
    },
    {
        "code": "MCB003",
        "name": "MCB Bank Limited",
        "swift_code": "MCBPPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Karachi Main Branch", "phone": "+922155555555"},
            {"branch_code": "002", "address": "Gulshan-e-Iqbal, Karachi", "phone": "+922166666666"}
        ]
    },
    {
        "code": "ABL004",
        "name": "Allied Bank Limited",
        "swift_code": "ABLAPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Karachi City Branch", "phone": "+922177777777"},
            {"branch_code": "002", "address": "North Nazimabad, Karachi", "phone": "+922188888888"}
        ]
    },
    {
        "code": "BAHL005",
        "name": "Bank Al Habib Limited",
        "swift_code": "BAHLPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Karachi Main Branch", "phone": "+922199999999"},
            {"branch_code": "002", "address": "Tariq Road, Karachi", "phone": "+922110101010"}
        ]
    },
    {
        "code": "SCB006",
        "name": "Standard Chartered Bank",
        "swift_code": "SCBLPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Abdullah Haroon Road, Karachi", "phone": "+922111111111"},
            {"branch_code": "002", "address": "Saddar, Karachi", "phone": "+922112121212"}
        ]
    },
    {
        "code": "FBL007",
        "name": "Faysal Bank Limited",
        "swift_code": "FAYSPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Karachi Main Branch", "phone": "+922113131313"},
            {"branch_code": "002", "address": "Gulistan-e-Jauhar, Karachi", "phone": "+922114141414"}
        ]
    },
    {
        "code": "BOP008",
        "name": "Bank of Punjab",
        "swift_code": "BPUNPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Karachi Main Branch", "phone": "+922115151515"},
            {"branch_code": "002", "address": "Malir, Karachi", "phone": "+922116161616"}
        ]
    },
    {
        "code": "SBL009",
        "name": "Summit Bank Limited",
        "swift_code": "SUMBPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Karachi Main Branch", "phone": "+922117171717"},
            {"branch_code": "002", "address": "Korangi, Karachi", "phone": "+922118181818"}
        ]
    },
    {
        "code": "JSBL010",
        "name": "JS Bank Limited",
        "swift_code": "JSBLPKKA",
        "country": "Pakistan",
        "branches": [
            {"branch_code": "001", "address": "Karachi Main Branch", "phone": "+922119191919"},
            {"branch_code": "002", "address": "Shahrah-e-Faisal, Karachi", "phone": "+922120202020"}
        ]
    }
]

for bank_data in pakistani_banks:
    bank = Bank.objects.create(
        code=bank_data["code"],
        name=bank_data["name"],
        swift_code=bank_data["swift_code"],
        country=bank_data["country"]
    )
    
    for branch_data in bank_data["branches"]:
        Branch.objects.create(
            bank=bank,
            branch_code=branch_data["branch_code"],
            address=branch_data["address"],
            phone=branch_data["phone"]
        )

print("Successfully inserted 10 Pakistani banks with branches!")