from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  # <-- Here
from rest_framework.authtoken.models import Token
from .models import Book
from .serializers import BookSerializer,UserSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import PermissionDenied


class BookListCreateView(APIView):
    #serializer_class=Bookseri
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response({'status':200,'payload':serializer.data})

#class RegisterUser(APIView):    
#    permission_classes = [IsAuthenticated]
#    def post(self, request):
#        serializer =UserSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            user = User.objects.get(username=serializer.data['username'])
#            token, create = Token.objects.get_or_create(user=user)
#            return Response({'status': 201, 'payload': serializer.data, 'token': token.key,'user_id':user.pk})
#        return Response({'status': 400, 'errors': serializer.errors})
#
class RegisterUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': 201, 'payload': serializer.data, 'token': token.key, 'user_id': user.pk})
        return Response({'status': 400, 'errors': serializer.errors})
    
class CreateBook(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response({'status': 201, 'payload': serializer.data})
        return Response({'status': 400, 'errors': serializer.errors})
    
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    def put(self,request,book_id):
        try:
            book = Book.objects.get(id=book_id)
            if book.author != request.user:
                raise PermissionDenied("You do not have permission to edit this book.")
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 200, 'payload': serializer.data})
            return Response({'status': 400, 'errors': serializer.errors})
        except Book.DoesNotExist:
            return Response({'status': 404, 'error': 'Book not found'})
    
    #permission_classes = [IsAuthenticated]    
    def delete(self,request,book_id):
        book = Book.objects.get(id=book_id)
        book.delete()
        return Response({'status': 204})


