from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view

from budgets.models import Transaction, MonthlyBudget, Expense
from categories.models import Category
from django.db.models import Sum
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    TransactionSerializer,
    CategorySerializer,
    MonthlyBudgetSerializer
)
# from .models import Transaction, Category, MonthlyBudget
from django.contrib import messages

from .forms import TransactionForm, CategoryForm, MonthlyBudgetForm

User = get_user_model()


# -------- API Views -------- #
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)  # use RegisterSerializer for API
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully!", "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Please provide both username and password"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=username, password=password)

    if user is not None:
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------- Template Views -------- #
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("user_home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")

@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, f"Transaction for {transaction.amount} saved successfully!")
            return redirect("user_home")
        else:
            messages.error(request, f"Form errors: {form.errors}")  # <-- This will show validation errors
    else:
        form = TransactionForm()

    return render(request, "budgets/add_transaction.html", {"form": form})

@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("user_home")
    else:
        form = CategoryForm()
    return render(request, "budgets/add_category.html", {"form": form})

@login_required
def user_home(request):
    user = request.user  

    # Total budgets across all categories for this user
    total_budget = MonthlyBudget.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Total expenses for this user
    total_expenses = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Total income/expense transactions for this user
    income = Transaction.objects.filter(user=user, type="income").aggregate(
        total=Sum('amount')
    )['total'] or 0

    expenses = Transaction.objects.filter(user=user, type="expense").aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Optional: per-category budgets
    categories_with_budgets = Category.objects.filter(user=user).annotate(
        total_budget=Sum('monthlybudget__amount')
    )
    transactions = Transaction.objects.filter(user=user).order_by('-transaction_date')

    context = {
        "total_budget": total_budget,
        "total_expenses": total_expenses,
        "income": income,
        "expenses": expenses,
        "categories_with_budgets": categories_with_budgets,
        "transactions": transactions,
    }

    return render(request, "budgets/user_home.html", context)

def logout_user(request):
    logout(request)
    return redirect("login_page")


@login_required
def add_budget(request):
    if request.method == "POST":
        form = MonthlyBudgetForm(request.POST, user=request.user)
        if form.is_valid():
            budget = form.save(commit=False)

            # Get the selected category
            category_id = request.POST.get("category")
            category = None
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                messages.error(request, f"Category with id={category_id} does not exist!")
                return redirect('add_budget')

            # DEBUG: Check FK IDs
            print(f"DEBUG: Budget month={budget.month}, year={budget.year}, amount={budget.amount}")
            print(f"DEBUG: Category ID={category.id}, Category user_id={category.user_id}")
            print(f"DEBUG: Request user ID={request.user.id}")

            budget.user = request.user
            budget.category = category

            try:
                budget.save()
                messages.success(request, f"The monthly budget “{budget.month}” was added successfully.")
            except Exception as e:
                messages.error(request, f"Error saving budget: {e}")
                print(f"Error saving budget: {e}")

            return redirect('user_home')
    else:
        form = MonthlyBudgetForm(user=request.user)

    return render(request, "budgets/add_budget.html", {"form": form})

class MonthlyBudgetViewSet(viewsets.ModelViewSet):
    queryset = MonthlyBudget.objects.all()
    serializer_class = MonthlyBudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)