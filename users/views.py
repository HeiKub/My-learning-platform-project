from .forms import ProfileForm  # We will create this form next
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from rest_framework.decorators import api_view
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

@api_view(['POST'])
def register_api(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.shortcuts import render

def home(request):
    return render(request, 'users/home.html')  # Path to the home template






# @login_required
# def profile(request):
#     profile = Profile.objects.get(user=request.user)

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             # Redirect to the user's profile page after saving
#             return redirect('user-profile')  # Make sure 'user-profile' is the correct URL name
#     else:
#         form = ProfileForm(instance=profile)

#     return render(request, 'users/profile.html', {'form': form, 'profile': profile})

# @login_required
# def profile(request):
#     # Check if the profile exists
#     try:
#         profile = Profile.objects.get(user=request.user)
#     except Profile.DoesNotExist:
#         profile = None  # No profile exists

#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             # Redirect to the user's profile page after saving
#             return redirect('user-profile')  # Ensure 'user-profile' is the correct URL name
#     else:
#         form = ProfileForm(instance=profile)

#     return render(request, 'users/profile.html', {'form': form, 'profile': profile})

# users/views.py
@login_required
def user_profile(request):
    profile = request.user.profile  # Get the profile of the logged-in user
    return render(request, 'users/user_profile.html', {'profile': profile})


@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful!'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def profile(request):
    # Try to get the profile; if it doesn't exist, create it
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Provide a success message based on whether it was created or updated
            if created:
                messages.success(request, 'Profile created successfully!')
            else:
                messages.success(request, 'Profile updated successfully!')
            return redirect('user-profile')  # Redirect to the user profile view
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/profile.html', {
        'form': form,
        'profile': profile,
        'is_first_time': created  # Pass this to the template to check if it's the first login
    })

from django.views.decorators.http import require_POST


@login_required
@require_POST  
def custom_logout(request):
    print("Logout view accessed") 
    logout(request)
    
    #return render(request, 'users/logout.html')
    return HttpResponseRedirect('/') 