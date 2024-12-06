from django.urls import path
from . import views

urlpatterns = [
    path('protected/', views.protected_view, name='protected_view'),  # 보호된 뷰 URL
]
