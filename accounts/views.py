from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect

def index(request):
    return create_account(request)

def create_account(request):
    def render_page(user_exists=False):
        params = {'user_exists': user_exists}
        return render(request, 'accounts/create_account.html', params)
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render_page(user_exists=True)
        else:
            user = User.objects.create_user(username, email, password)
            return redirect('main.views.home')
    else:
        return render_page()