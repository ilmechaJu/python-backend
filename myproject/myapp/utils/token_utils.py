import jwt
import datetime
from django.conf import settings

# 시크릿 키 설정
SECRET_KEY = settings.SECRET_KEY

def generate_access_token(user_id):
    """
    JWT Access Token 발행
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),  # 만료 시간 30분
        'iat': datetime.datetime.utcnow(),  # 발행 시간
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def generate_refresh_token(user_id):
    """
    Refresh Token 발행
    """
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # 7일 유효
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_access_token(token):
    """
    JWT Access Token 검증
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload  # 검증 성공 시 payload 반환
    except jwt.ExpiredSignatureError:
        return None  # 토큰 만료
    except jwt.InvalidTokenError:
        return None  # 유효하지 않은 토큰
