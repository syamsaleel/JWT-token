from django.urls import path
from .views import BookListCreateView,CreateBook,RegisterAPIView
#from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('', BookListCreateView.as_view(), name='bookcreate'),
    
    #path('register/', RegisterUser.as_view(), name='register'),
    path('registeruser/', RegisterAPIView.as_view(), name='register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api/token/', obtain_auth_token, name='token_obtain'),
    path('books/create/', CreateBook.as_view(), name='create_book'),
    path('books/<int:book_id>/', CreateBook.as_view(), name='book_update'),
    path('book/<int:book_id>/', CreateBook.as_view(), name='book_delete'),

]
