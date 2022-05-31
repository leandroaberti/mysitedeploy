from asyncio import constants
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .forms import UserForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def register(request):

    if request.method == 'POST':
        
        form = UserForm(request.POST)

        #print('User: ', request.POST.get('username'))
        #print('Email:', request.POST.get('email'))
        #print('PWD1: ', request.POST.get('password1'))
        #print('PWD2: ', request.POST.get('password2'))
        
        print('User: ', form['username'].value())
        print('Email:', form['email'].value())
        print('PWD1: ', form['password1'].value())
        print('PWD2: ', form['password2'].value())


        if form.is_valid():
            user = form.save()
            
            #username = form.cleaned_data.get('username')
            #password = form.cleaned_data.get('password2')


            return redirect('/myapp/products')
        else:
            error = form.errors
            print (form.errors)
            return render (request, 'users/register.html', {'form':form})

    form = UserForm()
    context = {
        'form': form,
    }

    return render(request, 'users/register.html', context)

@login_required # login required decoration 
def profile(request):
    return render(request, 'users/profile.html')


def create_profile(request):
    if request.method == 'POST':
        contact_number = request.POST.get('contact_number')
        image = request.FILES['upload']
        user = request.user

        profile = Profile(user=user, image=image, contact_number=contact_number)

        profile.save()

    return render(request, 'users/createprofile.html')

def seller_profile(request, id):
    
    seller = User.objects.get(id=id)
    
    context = {
        'seller':seller,
    }
    
    return render(request, 'users/seller_profile.html',context)