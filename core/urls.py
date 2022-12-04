from django.urls import path, include
from .views import(
    HomeView,
    ItemDetailView
)
app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name='homepage'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    
    ]