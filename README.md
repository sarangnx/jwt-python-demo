# Environment Variables

Put the variables in `.env` file

```bash
COGNITO_JWKS_URL="https://cognito-idp.<region>.amazonaws.com/<user-pool-id>/.well-known/jwks.json"
COGNITO_CLIENT_ID="cognito-client-id"
ISSUER="https://cognito-idp.<region>.amazonaws.com/<user-pool-id>"
```

# Running the app

```bash
docker compose up -d --build
```

# Invoking the API

```bash
curl -X GET http://localhost:5000/processor -H "Authorization: Bearer <token>"
```
