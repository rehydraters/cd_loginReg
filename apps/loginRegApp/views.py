from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *
import bcrypt

# the index function is called when root is visited
def index(request):
    return render(request, 'loginRegApp/index.html')

def register(request):
    errors = User.objects.basic_validator_reg(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    hash1 = bcrypt.hashpw(request.POST['pword'].encode(), bcrypt.gensalt())
    User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hash1)
    user = User.objects.last()
    request.session['logged_in'] = user.id
    return redirect('/success')

def login(request):
    errors = User.objects.basic_validator_login(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['logged_in'] = user.id
    return redirect('/success')

def success(request):
    return render(request, 'loginRegApp/success.html', { 'user': User.objects.get(id=request.session['logged_in']) })