# Mock analysis data for Commercial Lease Agreement

SAMPLE_ANALYSIS_DATA = {
    "document_metadata": {
        "title": "Commercial Office Lease Agreement",
        "parties": [
            "Vanguard Commercial Properties LLC (Landlord)",
            "Apex Technology Solutions Inc. (Tenant)"
        ],
        "date": "October 12, 2025",
        "summary": "A triple-net (NNN) commercial lease agreement for approximately 15,000 square feet of office space on the 4th floor of the Vanguard Tower, Seattle, WA. The lease term is 60 months (5 years) with a base rent starting at $35,000/month, subject to a 3% annual escalation. The tenant is responsible for a pro-rata share (12.5%) of building operating expenses, insurance, and taxes.",
        "governing_law": "State of Washington"
    },
    "key_terms": [
        {
            "term": "Lease Term",
            "definition": "The duration of the lease is 60 months, commencing on January 1, 2026, and expiring on December 31, 2030.",
            "location": "Section 2.2, Page 1"
        },
        {
            "term": "Base Rent",
            "definition": "Starting at $35,000 per month, due on the 1st of each calendar month, with a 3% annual increase compounded annually.",
            "location": "Section 3.1 & Schedule B, Page 2"
        },
        {
            "term": "Security Deposit",
            "definition": "A refundable security deposit of $70,000 is required upon execution of the lease, held as security for the performance of Tenant's obligations.",
            "location": "Section 4.1, Page 3"
        },
        {
            "term": "Triple Net (NNN) Share",
            "definition": "Tenant agrees to pay its pro-rata share (calculated as 12.5% based on occupied square footage) of all building operating expenses, insurance premiums, and real property taxes.",
            "location": "Section 5.2, Page 4"
        },
        {
            "term": "Permitted Use",
            "definition": "The premises shall be used solely for general professional offices, technology research, and ancillary administrative services.",
            "location": "Section 6.1, Page 5"
        },
        {
            "term": "Holdover Rent",
            "definition": "In the event the Tenant remains in possession of the premises after the expiration of the lease term without written consent, the holdover rent rate will be 150% of the last applicable base rent.",
            "location": "Section 18.2, Page 14"
        },
        {
            "term": "Option to Renew",
            "definition": "Tenant has one (1) option to renew the lease for an additional period of five (5) years, provided written notice is delivered to Landlord at least 270 days prior to expiration.",
            "location": "Section 21.1, Page 16"
        }
    ],
    "risks": [
        {
            "risk_id": "R-1",
            "severity": "Critical",
            "category": "Financial",
            "description": "High holdover rent penalty of 150% of base rent, which could lead to significant financial liability if lease relocation is delayed even by a few days.",
            "clause": "Section 18.2: 'If Tenant holds over after the expiration of the Term... Tenant shall pay to Landlord holdover rent equal to 150% of the Base Rent in effect immediately prior to such expiration.'",
            "mitigation": "Establish strict transition timeline milestones. Negotiate the holdover rate down to 125% or add a 15-day grace period at the normal rent rate."
        },
        {
            "risk_id": "R-2",
            "severity": "High",
            "category": "Legal",
            "description": "One-sided indemnification clause. Tenant must indemnify Landlord for all claims arising from the premises, except those due to Landlord's 'sole gross negligence'.",
            "clause": "Section 12.1: 'Tenant shall defend, indemnify, and hold Landlord harmless from any and all claims, damages, or liabilities arising from Tenant's use of the Premises... except to the extent caused by the sole gross negligence of Landlord.'",
            "mitigation": "Negotiate a mutual indemnification clause where each party indemnifies the other for claims resulting from their respective negligence, and delete the word 'sole'."
        },
        {
            "risk_id": "R-3",
            "severity": "High",
            "category": "Financial",
            "description": "No annual cap or limit on controllable operating expenses (CAM), exposing the tenant to potentially uncapped escalations in property management and building expenses.",
            "clause": "Section 5.3: 'Operating Expenses shall include all costs incurred by Landlord in the operation, maintenance, management, and repair of the Building... Tenant shall pay its pro-rata share of all such expenses.'",
            "mitigation": "Negotiate an annual cap (e.g., 5% non-cumulative) on controllable operating expenses (excluding taxes, utilities, and insurance)."
        },
        {
            "risk_id": "R-4",
            "severity": "Medium",
            "category": "Operational",
            "description": "Landlord has unrestricted access to the premises for inspections, repairs, and showings with only verbal notice, creating potential business disruptions.",
            "clause": "Section 14.4: 'Landlord and its agents shall have the right to enter the Premises at all reasonable times, upon verbal notice, to inspect the same, show to prospective buyers or tenants, or make repairs...'",
            "mitigation": "Request at least 24 hours prior written notice for all non-emergency entries and restrict showings to standard non-business hours unless accompanied by a tenant representative."
        },
        {
            "risk_id": "R-5",
            "severity": "Low",
            "category": "Compliance",
            "description": "Tenant must obtain Landlord's written consent prior to making any alterations or additions, even minor cosmetic updates like painting or putting up shelves.",
            "clause": "Section 8.1: 'Tenant shall not make any alterations, additions, or improvements in or to the Premises without Landlord's prior written consent, which consent shall not be unreasonably withheld.'",
            "mitigation": "Include a clause permitting 'Cosmetic Alterations' (e.g. painting, carpeting, shelving under a threshold of $15,000) without Landlord's prior consent."
        }
    ],
    "action_items": [
        {
            "action": "Pay Security Deposit of $70,000",
            "deadline": "Within 10 days of lease execution (due by October 22, 2025)",
            "responsible_party": "Accounts Payable / Finance Dept",
            "significance": "A fundamental requirement of lease execution. Failure to deposit on time constitutes an immediate material default."
        },
        {
            "action": "Submit Certificate of Insurance (COI)",
            "deadline": "At least 15 days prior to Commencement Date (due by December 17, 2025)",
            "responsible_party": "Risk Management Team",
            "significance": "Required before Tenant is granted access or keys to the premises for moving in. Must name Landlord as an additional insured."
        },
        {
            "action": "Perform Pre-Commencement Walkthrough Inspection",
            "deadline": "Between December 20, 2025, and December 30, 2025",
            "responsible_party": "Facilities Manager",
            "significance": "Essential to document pre-existing defects and condition of the premises to prevent disputes regarding restoration at lease end."
        },
        {
            "action": "Submit Written Notice of Renewal Option Option",
            "deadline": "On or before March 31, 2030 (270 days prior to lease expiration)",
            "responsible_party": "Legal Division / Corporate Real Estate",
            "significance": "The option to renew the lease for another 5 years is strictly forfeited if written notice is not delivered by this deadline."
        }
    ],
    "risk_scores": {
        "severity_counts": {
            "Critical": 1,
            "High": 2,
            "Medium": 1,
            "Low": 1
        },
        "category_counts": {
            "Financial": 2,
            "Legal": 1,
            "Operational": 1,
            "Compliance": 1
        }
    }
}
