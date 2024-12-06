from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def secure_view(request):
    return HttpResponse("로그인한 사용자만 볼 수 있습니다.")

@permission_required('myapp.can_edit')
def edit_view(request):
    return HttpResponse("권한이 있는 사용자만 볼 수 있습니다.")

@login_required
def protected_view(request):
    return HttpResponse("이 페이지는 인증된 사용자만 접근할 수 있습니다.")