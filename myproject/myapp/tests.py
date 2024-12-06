from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthenticationTest(TestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.login_url = reverse('login')  # 로그인 URL 이름 지정
        self.protected_url = reverse('protected_view')  # 인증이 필요한 뷰의 URL 이름 지정

    def test_login_successful(self):
        # 유효한 자격 증명으로 로그인 테스트
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # 리디렉션 상태 코드 확인

    # 리디렉션 후 상태 코드 확인 (optional)
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 200)  # 로그인 성공 시 상태 코드 확인


    def test_login_unsuccessful(self):
        # 잘못된 자격 증명으로 로그인 테스트
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  # 로그인 페이지로 리디렉션
        self.assertFalse('_auth_user_id' in self.client.session)  # 세션에 사용자 ID 없음

    def test_protected_view_redirect(self):
        # 인증되지 않은 사용자로 보호된 뷰 접근 시 리디렉션 확인
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리디렉션
        self.assertIn(reverse('login'), response.url)

    def test_protected_view_access(self):
        # 인증된 사용자로 보호된 뷰 접근 테스트
        self.client.login(username='testuser', password='password123')  # 로그인
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)  # 접근 성공
