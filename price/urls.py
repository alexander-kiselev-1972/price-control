from django.urls import path
from . import views


urlpatterns = [
    path('lek_search/', views.lek_search, name='lek_search'),
   # path('lek_price/<int: lek_id>/', )
]