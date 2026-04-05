from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
    read_only_fields = ['id']
    
class UserCreateSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
    write_only = True,
    min_length=8,
    styles = {'input_type': 'password'},
    )
  
  class Meta:
    model = User
    fields = ['username','email','password','role']
    
  def create(self,validated_data):
    return User.objects.create_user(**validated_data)
    
  def validate(self, value):
    allowed = [User.visitor,User.admin,User.analyst]
    if value not in allowed:
      serializer.ValidationError(
        f'Role must be one of {(',').join(allowed)}'
      )
    return allowed
    
    
    