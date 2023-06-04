from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.validators import UniqueValidator

from .models import Seller, User


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    BIN = serializers.IntegerField(required=False, validators=[UniqueValidator(queryset=Seller.objects.all())])
    business_name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2', 'username', 'phone_number', 'is_seller',
                  'BIN', 'business_name'
                  )
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def save(self):
        user = User(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone_number=self.validated_data['phone_number'],
            is_seller=self.validated_data['is_seller']
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        user.set_password(password)
        user.save()
        if user.is_seller:
            Seller.objects.create(user=user,
                                  BIN=self.validated_data['BIN'],
                                  business_name=self.validated_data['business_name'])
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Текущий пароль указан неверно'})

        return value


class SellerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ('BIN', 'business_name', 'bio', 'rating')
        extra_kwargs = {
            'rating': {'read_only':True}
        }


class UserProfileSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    seller = SellerProfileSerializer()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'phone_number', 'seller')

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(UserProfileSerializer, self).__init__(*args, **kwargs)






