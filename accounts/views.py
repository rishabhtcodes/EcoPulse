from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import UserRegistrationForm
from .models import UserProfile, FavoriteCity
from cities.models import City

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'dashboard:index')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password credentials.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                default_city=form.cleaned_data.get('default_city')
            )
            if profile.default_city:
                FavoriteCity.objects.get_or_create(user=user, city=profile.default_city)

            login(request, user)
            messages.success(request, f'Account successfully registered! Welcome to EcoPulse India.')
            return redirect('dashboard:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('dashboard:index')

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    favorites = FavoriteCity.objects.filter(user=request.user).select_related('city')
    all_cities = City.objects.all().order_by('name')

    if request.method == 'POST':
        default_city_id = request.POST.get('default_city')
        if default_city_id:
            city = City.objects.filter(id=default_city_id).first()
            if city:
                profile.default_city = city
                profile.save()
                messages.success(request, f'Default city updated to {city.name}.')
                return redirect('accounts:profile')

    context = {
        'profile': profile,
        'favorites': favorites,
        'all_cities': all_cities
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def toggle_favorite(request, city_id):
    city = get_object_or_404(City, id=city_id)
    fav = FavoriteCity.objects.filter(user=request.user, city=city).first()
    if fav:
        fav.delete()
        is_favorited = False
        msg = f'Removed {city.name} from your favorites.'
    else:
        FavoriteCity.objects.create(user=request.user, city=city)
        is_favorited = True
        msg = f'Added {city.name} to your favorites.'

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({'status': 'ok', 'favorited': is_favorited, 'message': msg})
    
    messages.success(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'cities:list'))
