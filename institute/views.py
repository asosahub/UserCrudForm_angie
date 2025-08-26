from django.shortcuts import render, get_object_or_404, redirect
from institute.forms.user_form import UserForm
from institute.forms.career_form import CareerForm
from institute.forms.clubs_form import ClubsForm
from institute.models import User, Career, Clubs

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


#Creacion de carrera
def create_career(request):
    if request.method == 'POST':
        form = CareerForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'institute/success_career.html')
    if request.method == 'GET':
        form = CareerForm()
        return render(request, 'institute/create_career.html', {'form': form})
    return render(request, 'institute/create_career.html')

#Creacion de clubes
def create_club(request):
    if request.method == 'POST':
        form = ClubsForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'institute/success_clubs.html')
    if request.method == 'GET':
        form = ClubsForm()
        return render(request, 'institute/create_clubs.html', {'form': form})
    return render(request, 'institute/create_clubs.html')

#lista de carreras
def career_list(request):
    careers = Career.objects.all()
    return render(request, 'institute/career_list.html', {'careers': careers})

#lista de clubes
def club_list(request):
    clubs = Clubs.objects.all()
    return render(request, 'institute/clubs_list.html', {'clubs': clubs})


#eliminar carreras
def delete_career(request, career_id):
    career = get_object_or_404(Career, pk=career_id)
    if request.method == 'POST':
        career.delete()
        return redirect('career_list')
    return render(request, 'institute/confirm_delete_career.html', {'career': career})

#eliminar clubes
def delete_club(request, club_id):
    club = get_object_or_404(Clubs, pk=club_id)
    if request.method == 'POST':
        club.delete()
        return redirect('clubs_list')
    return render(request, 'institute/confirm_delete_club.html', {'club': club})

#actualizar carreras
def update_carrer_modal(request, career_id):
    career = get_object_or_404(Career, pk=career_id)

    if request.method == 'POST':
        form = CareerForm(request.POST, instance=career)
        if form.is_valid():
            form.save()
            redirect('career_list')
        return redirect('career_list')
    

#actualizar clubes
def update_club_modal(request, club_id):
    club = get_object_or_404(Clubs, pk=club_id)

    if request.method == 'POST':
        form = ClubsForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            redirect('clubs_list')
        return redirect('clubs_list')