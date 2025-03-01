# Create your views here.
import json

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny

from api.models import UploadBookImage
from api.serializers import BooksSerializer, AuthorsSerializer, CategoriesSerializer, ImageSerializer, \
    CustomUserSerializer
from backend.models import Books, Authors, Categories, CustomUser

from django.http import Http404, HttpResponse
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView


class ListBooks(APIView):
    def get(self, request, format=None):
        permission_classes = [permissions.IsAuthenticated]
        book = Books.objects.all()
        serializer = BooksSerializer(book, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailBooks(APIView):
    def get_object(self, pk):
        try:
            return Books.objects.get(pk=pk)
        except Books.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        permission_classes = [permissions.IsAuthenticated]
        books = self.get_object(pk)
        serializer = BooksSerializer(books)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        books = self.get_object(pk)
        serializer = BooksSerializer(books, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        permission_classes = [permissions.IsAuthenticated]
        books = self.get_object(pk)
        serializer = BooksSerializer(books, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        books = self.get_object(pk)
        books.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListAuthors(APIView):
    def get(self, request, format=None):
        permission_classes = [permissions.IsAuthenticated]
        authors = Authors.objects.all()
        serializer = AuthorsSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AuthorsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailAuthors(APIView):
    def get_object(self, pk):
        try:
            return Authors.objects.get(pk=pk)
        except Authors.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        permission_classes = [permissions.IsAuthenticated]
        authors = self.get_object(pk)
        serializer = AuthorsSerializer(authors)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        authors = self.get_object(pk)
        serializer = AuthorsSerializer(authors, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        authors = self.get_object(pk)
        serializer = AuthorsSerializer(authors, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        authors = self.get_object(pk)
        authors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCategories(APIView):
    def get(self, request, format=None):
        permission_classes = [permissions.IsAuthenticated]
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CategoriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailCategories(APIView):
    def get_object(self, pk):
        try:
            return Categories.objects.get(pk=pk)
        except Categories.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        permission_classes = [permissions.IsAuthenticated]
        categories = self.get_object(pk)
        serializer = CategoriesSerializer(categories)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        categories = self.get_object(pk)
        serializer = CategoriesSerializer(categories, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        categories = self.get_object(pk)
        serializer = CategoriesSerializer(categories, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        categories = self.get_object(pk)
        categories.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageViewSet(ListAPIView):
    queryset = UploadBookImage.objects.all()
    serializer_class = ImageSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        image = UploadBookImage.objects.create(image=file)
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class CustomUserCreateAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)


class LogoutAPIVIEW(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()

        data = {
            'message': 'logout was successfull'
        }
        return Response(data=data, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token_type': 'token',
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# @api_view(['GET'])
# @permission_classes([IsStudent])
