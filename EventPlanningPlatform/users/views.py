from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import CustomUser
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})


# Özel Kullanıcı Kayıt Formu
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'birth_date', 
            'gender', 
            'phone_number', 
            'interests', 
            'profile_picture',
            'location',
        )
from django.contrib import messages

# Kullanıcı kayıt görünümü

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])  # Şifreyi doğru şekilde şifrele
            user.save()
            login(request, user)
            return redirect('home')
        else:
            print("Form geçerli değil:", form.errors)  # Hata varsa yazdır
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Kullanıcı giriş görünümü
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                print("Giriş başarılı:", user.username)  # Başarılı giriş
                return redirect('home')
        else:
            # Hataları ayrıntılı olarak göstermek için formdaki tüm hata mesajlarını yazdırın.
            print("Giriş başarısız:", form.errors)
            if 'username' in request.POST and 'password' in request.POST:
                print(f"Username: {request.POST['username']}, Password: {request.POST['password']}")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required(login_url='login')
def home(request):
    if request.user.is_superuser:
        return redirect('/admin/')  # Admin kullanıcıları otomatik olarak /admin sayfasına yönlendirilir
    return render(request, 'index.html')

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        # Doğum tarihini kontrol et ve geçerli olanı kaydet
        birth_date = request.POST.get('birth_date')
        if birth_date:
            try:
                # Doğum tarihini doğrudan modele atıyoruz, model otomatik olarak formatı doğrular.
                user.birth_date = birth_date
            except ValueError:
                messages.error(request, 'Doğum tarihi formatı geçersiz. Lütfen YYYY-AA-GG formatında giriniz.')
                return redirect('profile')
        else:
            user.birth_date = None

        user.gender = request.POST.get('gender')
        user.phone_number = request.POST.get('phone_number')
        user.interests = request.POST.get('interests')
         # Konumu güncelleme
        user.location = request.POST.get('location')

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profiliniz başarıyla güncellendi.')
        return redirect('profile')
    
    return render(request, 'profile.html', {'user': request.user})

# Kullanıcı çıkış görünümü
from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render

def events(request):
    return render(request, 'events.html')