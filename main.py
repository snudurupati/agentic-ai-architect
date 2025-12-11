from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn

app = FastAPI(title = "Enterprise CRM API")

# --- SECURITY CONFIGURATION ---
# We use HTTPBearer to extract the "Authorization: Bearer <token>" header
security = HTTPBearer()

# SIMULATED IDENTITY PROVIDER (IdP)
# In real life, this is Auth0/Okta checking a JWT signature.
# Here, we map tokens to permissions (Scopes).
VALID_TOKENS = {
    "super-agent-secret": {
        "user": "Agent-007",
        "scopes": ["read:orders", "write:refunds"]  # Can do everything
    },
    "junior-agent-secret": {
        "user": "Intern-Bot",
        "scopes": ["read:orders"]  # Can look, but CANNOT refund
    }
}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extracts the token and verifies it exists."""
    token = credentials.credentials
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail="Invalid Authentication Token")
    return VALID_TOKENS[token]

def has_scope(required_scope: str):
    """Dependency that checks if the user has the specific permission."""
    def scope_checker(user_data: dict = Depends(verify_token)):
        if required_scope not in user_data["scopes"]:
            raise HTTPException(
                status_code=403, 
                detail=f"Not Authorized. Missing scope: {required_scope}"
            )
        return user_data
    return scope_checker

# --- DATABASE MOCK ---
orders_db = {
    "ORD-123": {"status": "shipped", "customer": "Sreeram", "total": 150.00},
}

# --- PYDANTIC MODELS (TYpe Safety) ---
class OrderResponse(BaseModel):
    order_id: str
    status: str
    total: float

class RefundRequest(BaseModel):
    order_id: str
    reason: str

class RefundResponse(BaseModel):
    success: bool
    message: str
    refunded_amount: float

# --- ENDPOINTS ---
@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str, 
    user: dict = Security(has_scope("read:orders")) # <--- THE GUARD
):
    print(f"🔒 Access granted to {user['user']}")
    
    """Retrieves order details. Used by the Agent to check status."""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(order_id=order_id, **order)

# Requires "write:refunds" scope
@app.post("/refunds", response_model=RefundResponse)
async def process_refund(
    request: RefundRequest,
    user: dict = Security(has_scope("write:refunds")) # <--- THE GUARD
):
    print(f"💰 Refund authorized by {user['user']}")
    """Processes a refund. The Agent calls this to take action."""
    if request.order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Simulate business logic
    order = orders_db[request.order_id]

    return RefundResponse(
        success=True, 
        message=f"Refunded {request.reason}",
        refunded_amount=order['total'] # We fulfill the promise here
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)