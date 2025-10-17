from rest_framework import serializers
from .models import User, Career

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'age',
            'email',
            'career',
            'rol',
            'clubs'
        ]

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Debe ser mayor de edad")
        return value
    
    def validate_email(self, value):
        # Validar que el email no exista
        user_id = self.instance.id
        if User.objects.filter(email__iexact=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("Ya existe un usuario con este email")
        return value
    
    def validate(self, data):
        if data['first_name'] == data['last_name']:
            raise serializers.ValidationError("El nombre y el apellido no pueden ser iguales")
        return data
    

class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = [
            'id',
            'name'
        ]