import jwt
from config import Config

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImVtYWlsIjoidGVzdDEwQHRlc3RtYWlsLmNvbSIsInVpZCI6Ijc3YTIwN2UxLTMzN2YtNGM1MC05ZjA1LWZkMTMyY2M2NTlmYyJ9LCJleHAiOjE3NDcyODU3NDUuNTg4MTUyLCJyZWZyZXNoIjpmYWxzZSwiamlkIjoiZTU4ODczZjEtODIxNC00MzMzLWE3YmYtN2JiMmVjNGY4YWE4In0.ZXmReRZ0qceWvZ_cW088CyqXvYXP9L7hfnPYKCYo2MQ'

res = jwt.decode(jwt=token, key=Config.JWT_SECRET, algorithms=Config.JWT_ALGO)


print(res)