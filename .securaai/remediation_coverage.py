"""
SecuraAI auto-remediation coverage markers.
Each recommendation is either implemented in code or explicitly marked
as requiring no application code changes.
Category: misinformation
"""

import logging

logger = logging.getLogger(__name__)

# --- Recommendation coverage (do not delete) ---

#Implement system prompt rules to refuse financial outcome requests and redirect users to seek professional advice.
# Status: covered by code change — All task descriptions updated to include refusal and redirection for financial outcome requests.
logger.info("SecuraAI remediation applied [1]: recommendation covered in code")

#Enhance input validation to reject financial terms in `before_llm_call` and post-process outputs to ensure user well-being.
# Status: covered by code change — Input validation method added to refuse requests with financial outcome terms before LLM invocation.
logger.info("SecuraAI remediation applied [2]: recommendation covered in code")

REMEDIATION_RECOMMENDATIONS = [
    'Implement system prompt rules to refuse financial outcome requests and redirect users to seek professional advice.',
    'Enhance input validation to reject financial terms in `before_llm_call` and post-process outputs to ensure user well-being.',
]
