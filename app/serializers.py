from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Book,User


class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=100,
        min_length=2,
        validators=[UniqueValidator(queryset=Book.objects.all())]
    )
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    
    def validate_description(self, value):
        if len(value) < 15:
            raise serializers.ValidationError("Description must have at least 15 characters.")
        return value

    class Meta:
        model = Book
        fields = '__all__'
        


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, data):
        username = data['username']
        email = data['email']

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists.')

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists.')

        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user