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
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'password']
   