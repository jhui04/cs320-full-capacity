from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from fcapp.main.mongo_models import Device, Tenant, Status

# Create your views here.
def home_view(request):
    if not request.user.is_authenticated():
        #return redirect(reverse('login-view'))
        return redirect('/admin/login/?next=/')
    
    return render(request, "index.html")

def test_view(request):
    if not request.user.is_authenticated():
        #return redirect(reverse('login-view'))
        return redirect('/admin/login/?next=/')

    if request.GET.get("tenant_id"):
        tenant_id = request.GET.get("tenant_id")
        devices = Device.objects.filter(authorized__tenants=tenant_id)

        statuses = Status.for_user(request.user.id)
    else:
        tenant_id = Tenant.id_for_user(request.user.id)
        devices = Device.for_user(request.user.id)
        statuses = Status.for_user(request.user.id)
    return render(request, "test.html", {"tenant_id": tenant_id, "devices": devices, "statuses": statuses})




def login_view(request):
    if request.user.is_authenticated():
        return redirect(reverse('home-view'))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('home-view'))
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(reverse('home-view'))