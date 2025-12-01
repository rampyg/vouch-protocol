from fastapi import FastAPI, Header, HTTPException
from vouch import Verifier

app = FastAPI()
# (Mock key for demo)
verifier = Verifier('{"kty":"OKP","crv":"Ed25519","x":"..."}')

# MANIFESTO COMPLIANCE: Use 'X-Vouch-Auth' instead of 'Authorization'
@app.post("/agent/connect")
def connect_agent(x_vouch_auth: str = Header(None, alias="X-Vouch-Auth")):
    if not x_vouch_auth:
        raise HTTPException(status_code=400, detail="Missing X-Vouch-Auth header")
        
    is_valid, data = verifier.check_vouch(x_vouch_auth)
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Agent Reputation Check Failed")
        
    return {
        "status": "Connected", 
        "agent": data['sub'],
        "reputation": data['vc']['reputation_score']
    }
