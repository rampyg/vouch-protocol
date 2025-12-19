class N8NHelper:
    """
    Helper to generate n8n-compatible Python code blocks.
    """
    
    @staticmethod
    def get_code_node_snippet() -> str:
        return """
# n8n Python Code Node for Vouch Identity
# ---------------------------------------
# 1. Ensure 'vouch-protocol' is installed in your n8n environment
#    (docker run -e EXTERNAL_PYTHON_PACKAGES=vouch-protocol ...)

from vouch import Signer
import json
import os

# INPUT: The data coming from previous n8n nodes
# input_data = _input.all() # n8n specific

# CONFIG: Your Identity (Ideally set via env vars in n8n)
private_key = os.environ.get('VOUCH_PRIVATE_KEY')
did = os.environ.get('VOUCH_DID')

signer = Signer(private_key=private_key, did=did)

results = []
# for item in input_data:
#     # We sign the JSON content of the incoming item
#     payload = item.json
#     
#     # Generate the Vouch Token
#     token = signer.sign(payload)
#     
#     # Append the token to the output
#     item.json['vouch_token'] = token
#     results.append(item)

# return results
"""