from flask import Flask, request, jsonify
import requests
import jwt
from jwt.algorithms import RSAAlgorithm
from jwt.exceptions import InvalidTokenError
import os

COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_JWKS_URL = os.getenv('COGNITO_JWKS_URL')
ISSUER = os.getenv('ISSUER')

def get_jwks():
    return requests.get(COGNITO_JWKS_URL).json()

def get_public_key(kid):
    keys = get_jwks()['keys']
    for key in keys:
        if key['kid'] == kid:
            return RSAAlgorithm.from_jwk(key)
    raise Exception("Public key not found.")

def validate_jwt_token(token: str):
    try:
        unverified_header = jwt.get_unverified_header(token)
        public_key = get_public_key(unverified_header['kid'])

        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience=COGNITO_CLIENT_ID,
            issuer=ISSUER
        )
        return payload
    except InvalidTokenError as e:
        print(f"Token invalid: {e}")
        return None

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/processor', methods=['GET'])
def processor():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    payload = validate_jwt_token(token)
    if payload is None:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({"message": "Token is valid", "payload": payload})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
