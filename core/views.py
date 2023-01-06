from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from core.forms import ProfileForm

from .models import City, Profile

# Create your views here.

@login_required(login_url='/signin')
def index(request):
    current_user = Profile.objects.get(user=request.user)
    print(current_user)
    return render(request, 'index.html', {'user':current_user})

@login_required(login_url='/signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image'):
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('/settings')


    return render(request, 'setting.html', {'user_profile':user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # user_model = User.objects.filter(username=username)
        # print(user_model[0].id)
        # return render(request, 'signup.html')

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists.')
                return redirect('/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken.')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # login user and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # create a profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                print(user_model)
                new_profile.save()
                return redirect('/settings')
        else:
            messages.info(request, 'Password didn\'t match.')
            return redirect('/signup')

    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='/signin')
def logout(request):
    auth.logout(request)
    return redirect('/signin')



#======== EXTRA CODE FOR PRACTICE ========#
def person_update_view(request, pk):
    person = get_object_or_404(Profile, pk=pk)
    form = ProfileForm(instance=person)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.info(request, 'Profile updated successfully')
            return redirect('core:update_profile', pk=pk)
    return render(request, 'update_profile.html', {'form': form})

# AJAX
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id).all()
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)
