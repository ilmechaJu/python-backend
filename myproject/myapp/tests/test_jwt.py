import pytest
from myapp.utils.token_utils import generate_access_token, verify_access_token

@pytest.mark.django_db
def test_generate_access_token():
    user_id = 1  # 테스트용 사용자 ID
    token = generate_access_token(user_id)
    
    # 토큰이 생성되었는지 확인
    assert token is not None
    assert isinstance(token, str)

@pytest.mark.django_db
def test_verify_access_token():
    user_id = 1  # 테스트용 사용자 ID
    token = generate_access_token(user_id)
    
    # 토큰 검증
    payload = verify_access_token(token)
    assert payload is not None
    assert payload['user_id'] == user_id

@pytest.mark.django_db
def test_expired_access_token():
    from datetime import datetime, timedelta
    import jwt

    # 만료된 토큰 생성
    payload = {
        'user_id': 1,
        'exp': datetime.utcnow() - timedelta(seconds=1),  # 이미 만료된 시간
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, "testsecret", algorithm='HS256')
    
    # 만료된 토큰 검증
    result = verify_access_token(token)
    assert result is None  # 만료된 토큰은 None 반환
