from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, MonthlyBudget, Expense, Transaction
from django.contrib.auth.models import User
User = get_user_model()

# --------------------------
# USER SERIALIZER
# --------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'date_joined', 'password']
        extra_kwargs = {
            'password': {'write_only': True},   # Password should not be visible in GET responses
            'date_joined': {'read_only': True}, # Date joined is auto-set by Django, not editable by user
        }

    def create(self, validated_data):
        # Pop password from the validated data to set it securely
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # Hashes the password before saving
        user.save()
        return user


# --------------------------
# CATEGORY SERIALIZER
# --------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        # Ensure the category name is not empty or whitespace
        if not value.strip():
            raise serializers.ValidationError('Category name cannot be empty.')

        # Ensure the category name is unique (case-insensitive)
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError('Category already exists.')

        return value


# --------------------------
# MONTHLY BUDGET SERIALIZER
# --------------------------
class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = '__all__'

    def validate_amount(self, value):
        # Ensure the budget amount is greater than zero
        if value <= 0:
            raise serializers.ValidationError('Budget has to be greater than zero.')
        return value


# --------------------------
# EXPENSE SERIALIZER
# --------------------------
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

    def validate_amount(self, value):
        # Ensure expense amount is greater than zero
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_date(self, value):
        from datetime import date
        # Ensure the expense date is not set in the future
        if value > date.today():
            raise serializers.ValidationError('Expense date cannot be in the future.')
        return value


# --------------------------
# TRANSACTION SERIALIZER
# --------------------------
class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'transaction_date', 'type', 'description', 'user', 'category', 'category_name']

    def validate_amount(self, value):
        # Ensure transaction amount is greater than zero
        if value <= 0:
            raise serializers.ValidationError('Transaction amount must be greater than zero.')
        return value

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Don't return password in response

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Create a user with hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user