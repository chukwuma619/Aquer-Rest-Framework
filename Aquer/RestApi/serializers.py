from .models import User, Product, Category
from rest_framework import serializers

class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
    
    class Meta:
        model = User
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'