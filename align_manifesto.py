import os

# ==========================================
# 1. THE LICENSE (MIT for Adoption Phase)
# ==========================================
license_content = """MIT License

Copyright (c) 2025 Vouch Protocol Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# ==========================================
# 2. AUDITOR UPDATE (Add Reputation Score)
# ==========================================
auditor_code = """import json
import time
import uuid
from jwcrypto import jwk, jws

class Auditor:
    def __init__(self, private_key_json):
        self.signing_key = jwk.JWK.from_json(private_key_json)

    def issue_vouch(self, agent_data):
        # Default starting score for new agents
        reputation_score = agent_data.get('reputation_score', 50) 
        
        payload = {
            "jti": str(uuid.uuid4()),
            "sub": agent_data.get('did'),
            "iss": "did:web:vouch-authority",
            "nbf": int(time.time()),
            "exp": int(time.time()) + 86400, # 24 Hours
            "vc": { 
                "integrity_hash": agent_data.get('integrity_hash'),
                "reputation_score": reputation_score, # <-- NEW MANIFESTO FIELD
                "type": "Identity+Reputation"
            }
        }
        signer = jws.JWS(json.dumps(payload).encode('utf-8'))
        signer.add_signature(self.signing_key, None, json.dumps({"alg":"EdDSA"}), json.dumps({"kid":self.signing_key.key_id}))
        return {"certificate": signer.serialize(compact=True)}
"""

# ==========================================
# 3. EXAMPLE SERVER (X-Vouch-Auth Header)
# ==========================================
fastapi_code = """from fastapi import FastAPI, Header, HTTPException
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
"""

# --- WRITE FILES ---
with open("LICENSE", "w") as f:
    f.write(license_content)

with open("vouch/auditor.py", "w") as f:
    f.write(auditor_code)

with open("examples/fastapi_server.py", "w") as f:
    f.write(fastapi_code)

print("✅ Codebase aligned with Vouch Manifesto v1.0")
print("   - Added MIT License")
print("   - Added Reputation Score to Auditor")
print("   - Updated Examples to use X-Vouch-Auth header")
