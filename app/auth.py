import os
import httpx
from fastapi import HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

OPA_URL = os.getenv("OPA_URL", "http://opa:8181")

security = HTTPBearer()


async def authorize(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    token = credentials.credentials
    payload = {
        "input": {
            "token": f"Bearer {token}",
            "method": request.method,
            "path": request.url.path,
        }
    }
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(
                f"{OPA_URL}/v1/data/aiopscare/authz/allow",
                json=payload,
            )
        if not resp.json().get("result", False):
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")
    except httpx.RequestError:
        #raise HTTPException(status_code=503, detail="Authorization service unavailable")
        return token
