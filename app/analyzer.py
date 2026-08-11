import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# ---------------------------------------------------------------------------
# Pydantic Schema — defines the structured JSON output from Gemini
# ---------------------------------------------------------------------------

class DocumentMetadata(BaseModel):
    title: str = Field(description="The legal title of the document or contract.")
    document_type: str = Field(description="The type of legal agreement (e.g., Commercial Lease, Employment Agreement, NDA, Service Agreement, Software License).")
    parties: List[str] = Field(description="All parties involved in the agreement with their respective roles (e.g., 'Big Realty Inc. (Landlord)', 'Little Startup LLC (Tenant)').")
    date: str = Field(description="The execution date or effective date of the agreement. Use 'Not Specified' if missing.")
    term_duration: str = Field(description="The duration or term of the agreement (e.g., '24 months', 'At-will', 'Not Specified').")
    summary: str = Field(description="A detailed executive summary of the document (3-5 sentences) covering core purpose, scope, key financial terms, critical obligations, and unique characteristics.")
    governing_law: str = Field(description="The state, country, or jurisdiction whose laws govern the agreement. Use 'Not Specified' if missing.")
    overall_risk_rating: str = Field(description="An overall risk assessment of the document: 'Low Risk', 'Moderate Risk', 'High Risk', or 'Very High Risk' — justify in the summary.")

class KeyTerm(BaseModel):
    term: str = Field(description="The legal term, definition, or key clause heading.")
    definition: str = Field(description="A thorough explanation of what this term means in the context of this specific contract, including any notable nuances or unusual deviations from standard practice.")
    location: str = Field(description="The section, article, or clause number where this term appears.")
    significance: str = Field(description="Why this term is legally important and how it impacts the rights and obligations of the parties.")

class Risk(BaseModel):
    risk_id: str = Field(description="Unique risk ID: R-001, R-002, etc.")
    severity: str = Field(description="Severity level: Critical, High, Medium, or Low.")
    category: str = Field(description="Area of impact: Financial, Legal, Operational, Compliance, Intellectual Property, Privacy, Termination, or Other.")
    title: str = Field(description="A short, punchy title for the risk (max 10 words), e.g., 'Uncapped Liability Exposure', 'Unilateral Termination Without Cause'.")
    description: str = Field(description="A comprehensive description of why this clause is risky, what unfavorable outcome it could cause, and which party bears the burden.")
    clause: str = Field(description="The verbatim quote or close paraphrase from the contract text that creates this risk.")
    impact: str = Field(description="The tangible financial, legal, or operational impact if this risk materializes (e.g., 'potential liability up to $500k with no cap').")
    mitigation: str = Field(description="Specific, actionable negotiation strategy to mitigate this risk (e.g., 'Request a mutual liability cap equal to 12 months of contract value; add a force majeure carve-out').")
    probability: str = Field(description="Likelihood of this risk occurring: High, Medium, or Low.")

class ActionItem(BaseModel):
    action_id: str = Field(description="Unique action ID: A-001, A-002, etc.")
    action: str = Field(description="The specific legal obligation or task that must be completed.")
    deadline: str = Field(description="The exact deadline or time frame as stated in the contract.")
    responsible_party: str = Field(description="The party responsible for this action.")
    priority: str = Field(description="Priority level: Immediate, High, Medium, or Routine.")
    significance: str = Field(description="The legal, financial, or operational consequence of missing this deadline or failing to complete this action.")
    reference_clause: str = Field(description="The section or clause that creates this obligation.")

class LegalAnalysis(BaseModel):
    document_metadata: DocumentMetadata
    key_terms: List[KeyTerm]
    risks: List[Risk]
    action_items: List[ActionItem]

# ---------------------------------------------------------------------------
# Main Analysis Function
# ---------------------------------------------------------------------------

DEFAULT_MODEL = "gemini-3.1-flash-lite-preview"
FALLBACK_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash"
]

def _compute_risk_scores(analysis_dict: dict) -> dict:
    """Computes aggregate risk scores and category breakdowns from the extracted risks list."""
    risks_list = analysis_dict.get("risks", [])
    sev_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    cat_counts = {}

    for r in risks_list:
        raw_sev = str(r.get("severity", "Medium")).strip().capitalize()
        if raw_sev in sev_counts:
            sev_counts[raw_sev] += 1
        else:
            sev_counts["Medium"] += 1

        raw_cat = str(r.get("category", "General")).strip().title()
        cat_counts[raw_cat] = cat_counts.get(raw_cat, 0) + 1

    # Composite score calculation (Critical=15, High=8, Medium=3, Low=1)
    raw_score = (
        sev_counts["Critical"] * 15 +
        sev_counts["High"] * 8 +
        sev_counts["Medium"] * 3 +
        sev_counts["Low"] * 1
    )
    overall_score = min(100, max(5, raw_score)) if risks_list else 0

    analysis_dict["risk_scores"] = {
        "severity_counts": sev_counts,
        "category_counts": cat_counts,
        "overall_score": overall_score
    }
    return analysis_dict


def analyze_legal_text(document_text: str, custom_api_key: str = None, model_name: str = None) -> dict:
    """
    Submits extracted legal text to the Gemini API for structured risk assessment.

    Args:
        document_text (str): Full text of the legal document.
        custom_api_key (str, optional): User-supplied API key. Falls back to env var.
        model_name (str, optional): Specific model name. Defaults to gemini-3-flash-preview.

    Returns:
        dict: Parsed and validated legal analysis dictionary.
    """
    api_key = custom_api_key or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "Gemini API Key is not set. Please provide a key in the `.env` file "
            "or enter it in the sidebar settings."
        )

    # Use new google.genai client
    client = genai.Client(api_key=api_key)

    # Resolve model — default to gemini-3-flash-preview, only override if explicitly passed
    resolved_model = model_name if model_name else DEFAULT_MODEL

    prompt = f"""You are a senior legal counsel, contract analyst, and enterprise risk advisor with 20+ years of experience.

Your task is to conduct a comprehensive legal document audit and extract deeply structured insights from the contract text below.

## ANALYSIS REQUIREMENTS

### 1. Document Metadata
- Identify document type, all parties with their roles, dates, term/duration, governing law
- Assign an overall risk rating based on a holistic assessment
- Write a detailed executive summary covering all key elements

### 2. Key Terms & Definitions (extract 8-15 terms)
- Include all legally significant clauses: payment terms, IP ownership, termination conditions, indemnification, limitation of liability, warranties, confidentiality, dispute resolution, renewal/rollover conditions
- For each term: provide definition, clause location, and legal significance
- Flag any term that deviates significantly from market-standard practice

### 3. Risk Identification (identify ALL risks — be thorough)
For EACH risk:
- Assign a unique Risk ID (R-001, R-002, etc.)
- Give it a punchy descriptive title
- Classify severity: Critical (could cause financial ruin or criminal liability), High (significant financial/legal exposure), Medium (notable but manageable), Low (minor compliance notes)
- Categorize: Financial, Legal, Operational, Compliance, Intellectual Property, Privacy, Termination, or Other
- Quote the exact problematic clause
- Estimate tangible impact (quantify where possible)
- Provide a concrete negotiation/mitigation strategy
- Estimate probability of the risk materializing

Look specifically for:
- Uncapped or asymmetric liability provisions
- Unilateral termination or modification rights
- Auto-renewal clauses with short opt-out windows
- Holdover penalties disproportionate to base rates
- Broad indemnification obligations
- IP assignment clauses that are too wide
- Non-compete / non-solicitation overreach
- Dispute resolution clauses that favor the drafter
- Missing force majeure or material adverse change provisions
- Penalties for late payment without symmetrical late delivery provisions
- Confidentiality obligations that are perpetual or overly broad

### 4. Action Items (identify ALL obligations)
- Include all time-sensitive obligations, deliverables, payment milestones, notice requirements, renewal decisions, compliance filings
- Assign priority: Immediate (within 7 days), High (within 30 days), Medium (within 90 days), Routine (ongoing)
- Reference the specific clause creating each obligation

---

## DOCUMENT TEXT:
---
{document_text[:40000]}
---

Respond ONLY with valid JSON matching the requested schema. Be comprehensive, specific, and legally precise. Do not truncate or summarize risks — identify every significant one.
"""

    try:
        response = client.models.generate_content(
            model=resolved_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=LegalAnalysis,
                temperature=0.1,
            )
        )

        analysis_dict = json.loads(response.text)
        return _compute_risk_scores(analysis_dict)

    except Exception as e:
        error_msg = str(e)
        # If model not found, try fallbacks
        if "not found" in error_msg.lower() or "404" in error_msg or "invalid" in error_msg.lower():
            for fallback in FALLBACK_MODELS:
                try:
                    response = client.models.generate_content(
                        model=fallback,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=LegalAnalysis,
                            temperature=0.1,
                        )
                    )
                    analysis_dict = json.loads(response.text)
                    return _compute_risk_scores(analysis_dict)
                except Exception:
                    continue
        raise RuntimeError(f"Gemini API error: {error_msg}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Testing Gemini Client configuration...")
        test_key = os.getenv("GEMINI_API_KEY")
        if not test_key:
            print("ERROR: GEMINI_API_KEY env var not set.")
            sys.exit(1)

        test_text = """
        COMMERCIAL OFFICE LEASE AGREEMENT
        This Lease is executed on June 1, 2026, between Big Realty Inc. (Landlord) and Little Startup LLC (Tenant).
        Governing Law: The laws of the State of California.
        Section 3. Base Rent. Tenant shall pay Base Rent of $5,000 per month, due on the 1st of each month.
        Section 12. Holdover. If Tenant holds over after expiration without written consent, Tenant shall pay rent equal to 200% of Base Rent.
        Section 15. Security Deposit. Tenant must deliver $10,000 within 5 days of signing.
        Section 18. Indemnification. Tenant shall indemnify, defend, and hold harmless Landlord against any and all claims arising from Tenant's use of the premises, with no cap on liability.
        """
        try:
            print(f"Submitting request to {DEFAULT_MODEL}...")
            result = analyze_legal_text(test_text, test_key)
            print("\n--- TEST SUCCESSFUL ---")
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(f"\n--- TEST FAILED ---\nError: {e}")
    else:
        print("Usage: python app/analyzer.py --test  (requires GEMINI_API_KEY in env)")
