from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from base.models import Group, Friend, Expense
from django.contrib.auth.models import User
#from .models import Expense, Group
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    """View to handle user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, 'Registration successful.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    groups = request.user.groups.all()
    return render(request, 'dashboard.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        group = Group.objects.create(name=name)
        group.members.add(request.user)
        return redirect('dashboard')
    return render(request, 'create_group.html')


@login_required
def add_expense(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users_in_group = group.members.all()
    
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = float(request.POST.get('amount'))
        paid_by_user_id = int(request.POST.get('paid_by'))
        participant_ids = request.POST.getlist('participants')

        paid_by_user = User.objects.get(id=paid_by_user_id)
        participants = User.objects.filter(id__in=participant_ids)
        
        # Create and save the expense
        expense = Expense.objects.create(
            description=description,
            amount=amount,
            paid_by=paid_by_user,
            group=group
        )
        expense.participants.set(participants)
        expense.save()

        return redirect('dashboard')
    
    return render(request, 'add_expense.html', {'group': group, 'users_in_group': users_in_group})

def calculate_balances(group):
    balances = {}
    for member in group.members.all():
        balances[member.username] = 0
    
    expenses = Expense.objects.filter(group=group)
    for expense in expenses:
        split_amount = expense.amount / expense.participants.count()
        balances[expense.paid_by.username] += expense.amount
        
        for participant in expense.participants.all():
            balances[participant.username] -= split_amount
    
    return balances

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    balances = calculate_balances(group)
    return render(request, 'group_detail.html', {'group': group, 'balances': balances})


