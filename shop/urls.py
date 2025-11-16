from django.urls import path
from .views import *
urlpatterns = [
    path("",index,name="home"),
    path("register/",Register,name="Register"),
    path("Signin/", Login, name="Login"),
    path('Logout/',Logout,name='Logout'),
    path('about/', About, name='About'),
    path('Contact/',Views_Contact,name='Contact'),
    path('Gallery/', Views_Gallery, name='Gallery'),
    path('carusel/',Carusel,name='carusel'),
    path('shop/', Views_shop, name='shop'),
    path('products/<int:pk>/',Detail,name='Detail'),
    path('likes/',likes,name='likes'),
    path('likes/<int:pk>/',user_like,name='user_like')



]