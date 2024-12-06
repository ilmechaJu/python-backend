from django.urls import path
from . import views
from .views import SignupView, secure_view, edit_view

urlpatterns = [
    path('protected/', views.protected_view, name='protected_view'),  # 보호된 뷰 URL
    path('login/', views.login_view, name='login'),
    path('refresh-token/', views.refresh_token_view, name='refresh_token'),
    path('signup/', SignupView.as_view(), name='signup'),    
    path('secure/', secure_view, name='secure'),
    path('edit/', edit_view, name='edit'),
]
