from django.shortcuts import render, get_object_or_404, redirect
from institute.forms.user_form import UserForm
from institute.models import User

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'institute/success.html')
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'institute/create_user.html', {'form': form})
    return render(request, 'institute/create_user.html')


def update_user(request, user_id):
    #busca el usurio por id, devuelve un 404 si no lo encuentra
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user = get_object_or_404(User, pk=user_id)

        #crea el formulario con los datos del usuario
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            #muestra html de exito
            return render (request, 'institute/success_update.html', {'user': user})
    else:
        #si es un GET, muestra el formulario con los datos del usuario
        form = UserForm(instance=user)
    #renderiza el formulario con los datos del usuario
    return render(request, 'institute/update_user.html', {'form': form, 'user': user})

def user_list(request):
    users = User.objects.all()
    return render(request, 'institute/user_list.html', {'users': users})

def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'institute/confirm_delete.html', {'user': user})