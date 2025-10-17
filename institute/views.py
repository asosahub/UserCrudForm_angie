from django.shortcuts import render, get_object_or_404, redirect
from institute.forms.user_form import UserForm
from institute.forms.career_form import CareerForm
from institute.forms.clubs_form import ClubsForm
from institute.forms.login_form import UserLoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from institute.models import User, Career, Clubs
import requests
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, CareerSerializer


#LOGIN
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    auth_login(request, user, backend='institute.backends.UserBackend')
                    return redirect ('dashboard')
                else:
                    form.add_error('password', 'Credenciales invalidas')
            except User.DoesNotExist:
                form.add_error('email', 'Usuario no encontrado')
    else:
        form = UserLoginForm()

    return render(request, 'login/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')


def check_rol_admin(user):
    return user.is_authenticated and user.rol.rol == 'Administrador'

def check_rol_estudiante(user):
    return user.is_authenticated and user.rol.rol == 'Estudiante'

def check_rol_invitado(user):
    return user.is_authenticated and user.rol.rol == 'Invitado'


#Redirige al dashboard segun el rol
@login_required
def dashboard(request):
    user = request.user

    if user.rol.rol == 'Administrador':
        return redirect('dashboard_admin')
    elif user.rol.rol == 'Estudiante':
        return redirect('dashboard_estudiante')
    elif user.rol.rol == 'Invitado':
        return redirect('dashboard_invitado')
    else:
        #rol no reconocido y redirige a login
        auth_login(request)
        return redirect('login')
    

#dashboards especificos por rol
@login_required
@user_passes_test(check_rol_admin)
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html', {'user': request.user})

@login_required
@user_passes_test(check_rol_estudiante)
def dashboard_estudiante(request):
    return render(request, 'dashboard/estudiante.html', {'user': request.user})

@login_required
@user_passes_test(check_rol_invitado)
def dashboard_invitado(request):
    return render(request, 'dashboard/invitado.html', {'user': request.user})





def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #no guarda todavia
            user.set_password(form.cleaned_data['password']) #encripta
            user.save()
            form.save_m2m() #guarda relaciones m2m (clubs)
            return render(request, 'institute/success.html')
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'institute/create_user.html', {'form': form})
    return render(request, 'institute/create_user.html')


def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            if password:  # solo actualiza si se escribió algo
                updated_user.set_password(password)
            else:
                # Mantener la contraseña actual si el campo está vacío
                updated_user.password = user.password
            updated_user.save()
            form.save_m2m()
            return render(request, 'institute/success_update.html', {'updated_user': updated_user})
    else:
        form = UserForm(instance=user)

    return render(request, 'institute/update_user.html', {'form': form, 'user': user})

#ENDPOINT PARA USOS DE SERIALIZER

#actualizar usuario
@api_view(['PUT'])
def api_update_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
    
    serializer = UserSerializer(user, data=request.data)
    #realiza validacion
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)

#crear carrera
@api_view(['POST'])
def api_create_career(request):
    serializer = CareerSerializer(data=request.data)
    if serializer.is_valid():
        career = serializer.save() #guarda en la bd
        return Response (CareerSerializer(career).data, status=201)
    return Response(serializer.errors, status=400)



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
    




#CONSUMIR API PUBLICA (GENSHIN IMPACT)

def genshin_api_view(request):
    try:
        
        url = "https://genshin.jmp.blue/characters"
        response = requests.get(url)
        response.raise_for_status()
        characters = response.json()

        # PERSONAJE RANDOM
        random_character_name = random.choice(characters) if characters else None
        random_character_details = None
        
        if random_character_name:
            char_url = f"https://genshin.jmp.blue/characters/{random_character_name}"
            char_response = requests.get(char_url)
            random_character_details = char_response.json()

        context = {
            'characters': characters,
            'total_characters': len(characters),
            'first_character': random_character_details,
            'first_character_name': random_character_name,
            'api_url': url
        }

        return render(request, 'institute/genshin_api.html', context)
    
    except Exception as e:
        return render(request, 'institute/genshin_api.html', {
            'error': f"Error: {str(e)}"
        })
    