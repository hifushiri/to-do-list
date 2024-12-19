from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import todo
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = todo(user=request.user, name=task)
        new_todo.save()

    all_todos = todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todoapp/todo.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Raise error if pasword is too short (<4)
        if len(password) < 4:
            messages.error(request, 'The given password must be at least 4 characters long.')
            return redirect('register')
        
        # Raise error if given username is already used
        get_all_users_by_username = User.objects.filter(username=username)
        if get_all_users_by_username:
            messages.error(request, 'The given username is already in use.')
            return redirect('register')

        # If no errors save user to DB
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        # Redirect to login page after account creation
        messages.success(request, 'Account succsessfully created.')
        return redirect('login')
    return render(request, 'todoapp/register.html', {})

def logoutpage(request):
    logout(request)
    return redirect('login')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home-page')
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home-page')
        else:
            messages.error(request, 'User does not exist.')
            return redirect('login')
        
    return render(request, 'todoapp/login.html', {})

@login_required
def delete_task(request,id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.delete()
    return redirect('home-page')

@login_required
def update(request, id):
    get_todo = todo.objects.get(user=request.user, id=id)
    get_todo.status = not get_todo.status
    get_todo.save()
    return redirect('home-page')
