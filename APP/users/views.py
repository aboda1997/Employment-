from django.shortcuts import render ,  redirect

# Create your views here.

from  .forms import RegistrationForm , UserUpdateForm 

def register(request): 
    user = request.user
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.recruiter = user
            data.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    context = {
       
        'form': form,
    }
    return render(request, 'registration/register.html', context)


def edit (request): 
    you = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=you)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
    else:
        form = UserUpdateForm(instance=you)
    context = {
        'form': form,
    }
    return render(request, 'users/edit_user.html', context)