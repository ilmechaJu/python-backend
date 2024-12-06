from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Django 기본 User 모델을 확장한 Custom User 모델
    """
    # 필요 시 추가 필드 정의
    pass
