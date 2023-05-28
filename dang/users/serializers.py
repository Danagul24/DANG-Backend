from rest_framework import serializers
from accounts.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'phone_number')
        write_only_fields = ('password',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active')

