from django.contrib.auth.models import Group
from rest_framework import serializers

from api.models import UploadBookImage
from backend.models import Books, Authors, Categories, CustomUser


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'


class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadBookImage
        fields = ('image',)


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'email',
            'password'
        ]

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        group = Group.objects.get(name='Student')
        user.groups.add(group)
        user.save()
        return user