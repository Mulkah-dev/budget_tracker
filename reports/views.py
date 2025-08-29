from django.shortcuts import render
from django.db.models import Sum, Case, When, DecimalField
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from budgets.models import Transaction

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def transaction_summary(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    # ✅ Query params
    month = request.query_params.get("month")
    year = request.query_params.get("year")
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")

    # ✅ Filtering logic
    if month and year:
        transactions = transactions.filter(
            transaction_date__month=month,
            transaction_date__year=year
        )
    elif year:
        transactions = transactions.filter(transaction_date__year=year)

    if start_date and end_date:
        transactions = transactions.filter(
            transaction_date__range=[start_date, end_date]
        )

    summary = transactions.aggregate(
        total_income=Sum(
            Case(
                When(type="income", then="amount"),
                output_field=DecimalField()
            )
        ),
        total_expenses=Sum(
            Case(
                When(type="expense", then="amount"),
                output_field=DecimalField()
            )
        )
    )

    total_income = summary["total_income"] or 0
    total_expenses = summary["total_expenses"] or 0
    balance = total_income - total_expenses

    return Response({
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance
    })
