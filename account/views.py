from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def login(request):
    return render(request, 'account/login.html')