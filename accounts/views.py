from urllib.parse import urlencode

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.hashers import check_password, identify_hasher, make_password

from .forms import UserForm, UserProfileForm
from .models import User, UserProfile


def _safe_next_url(request):
    raw = (request.POST.get('next') or request.GET.get('next') or '').strip()
    if raw.startswith('/') and not raw.startswith('//'):
        return raw
    return ''


def _credentials_match(user, raw_password):
    if check_password(raw_password, user.password):
        return True
    try:
        identify_hasher(user.password)
    except ValueError:
        if raw_password == user.password:
            user.password = make_password(raw_password)
            user.save(update_fields=['password'])
            return True
    return False


def register(request):
    if request.method == 'GET':
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})

    elif request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.password = make_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(f"{reverse('login')}?{urlencode({'next': reverse('shop')})}")
        return render(
            request,
            'accounts/register.html',
            {'user_form': user_form, 'profile_form': profile_form},
        )

    user_form = UserForm()
    profile_form = UserProfileForm()
    return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})


def login(request):
    if request.method == 'GET':
        user_form = UserForm()
        return render(
            request,
            'accounts/login.html',
            {'user_form': user_form, 'next': _safe_next_url(request)},
        )
    elif request.method == 'POST':
        user_form = UserForm(request.POST)
        email = (request.POST.get('email') or '').strip()
        password = request.POST.get('password') or ''

        if not email or not password:
            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Please enter both email and password.',
                    'next': _safe_next_url(request),
                },
            )

        user = User.objects.filter(email__iexact=email).first()
        if user is None or not _credentials_match(user, password):
            return render(
                request,
                'accounts/login.html',
                {
                    'error': 'Invalid email or password.',
                    'next': _safe_next_url(request),
                },
            )

        request.session['user_id'] = user.id
        next_url = _safe_next_url(request)
        if next_url:
            return redirect(next_url)
        if user.role == 'admin':
            return redirect('admin_dashboard')
        return redirect('user_dashboard')
    return render(
        request,
        'accounts/login.html',
        {'user_form': user_form, 'next': _safe_next_url(request)},
    )
        

def logout(request):
    request.session.flush()
    return redirect('shop')

def user_dashboard(request):
    uid = request.session.get("user_id")
    if not uid:
        return redirect('login')
    try:
        User.objects.get(pk=uid)
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    return render(request, 'accounts/user_dashboard.html')

def admin_dashboard(request):
    uid = request.session.get("user_id")
    if not uid:
        return redirect('login')
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        request.session.flush()
        return redirect('login')
    if user.role != "admin":
        return redirect('user_dashboard')
    return render(request, 'accounts/admin_dashboard.html')


    