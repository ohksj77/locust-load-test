import uuid, requests
from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        """회원가입 API 호출 및 JWT 토큰 수신"""
        response: requests.Response = self.client.post("/api/v1/auth/save", json={
                "nickname": f"use{str(uuid.uuid4())[0:3]}",
                "profileImage": "profileImage_dummy",
                "deviceToken": "deviceToken_dummy",
                "oauthRequest": {
                    "token": f"{uuid.uuid4()}",
                    "authType": "APPLE"
                }
                }, headers={'Content-Type': 'application/json'})
        
        self.token = response.json()['tokenDto']['accessToken']

    @task
    def access_protected_resource(self):
        """JWT 토큰을 헤더에 추가하여 테스트하고자 하는 백엔드 서버 API 부하테스트"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/places/surround?latitude=37.527019&longitude=126.934416&page=1", headers=headers)
