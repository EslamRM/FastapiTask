from fastapi import APIRouter, HTTPException
from app.utils.token_utils import revoke_token
from app.schemas.auth import TokenRevokeRequest

router = APIRouter()

@router.post("/revoke-refresh-token")
async def revoke_refresh_token(data: TokenRevokeRequest):
    success = await revoke_token(data.refresh_token)
    if not success:
        raise HTTPException(status_code=400, detail="Token revocation failed")
    return {"message": "Token revoked successfully"}
