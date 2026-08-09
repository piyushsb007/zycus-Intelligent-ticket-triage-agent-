# =============================================================================================
# Evaluation Test Cases
# =============================================================================================

# ticket.json
TASK1_TESTS = [
    {
        "id": "T1-01",
        "subject": "Cannot log in after SSO migration",
        "body": "All users receive invalid SAML assertions after Okta migration.",
        "expected": {
            "product_area": "Authentication",
            "urgency_tier": "P1"
        }
    },
    {
        "id": "T1-02",
        "subject": "Invoice amount incorrect",
        "body": "We were charged twice for the same subscription period.",
        "expected": {
            "product_area": "Billing"
        }
    },
    {
        "id": "T1-03",
        "subject": "API endpoint returns 500",
        "body": "Production webhook requests fail with HTTP 500.",
        "expected": {
            "product_area": "API Platform",
            "urgency_tier": "P2"
        }
    },
    {
        "id": "T1-04",
        "subject": "Bulk archive request",
        "body": "Need bulk archive operations in DataBridge Pro Data Ingestion.",
        "expected": {
            "product_area": "Data Ingestion"
        }
    },
    # Adversarial / ambiguous
    {
        "id": "T1-05-ADV",
        "subject": "Something is not working",
        "body": "Please help, it fails sometimes.",
        "expected": {
            "urgency_tier": "P3"
        }
    }
]
# account.json
TASK2_TESTS = [
    {
        "id": "T2-01",
        "account_id": "ACC-3336",
        "criteria": [
            "Company:",
            "Omni Consumer Products",
            "Overall risk:"
        ]
    },
    {
        "id": "T2-02",
        "account_id": "ACC-3336",
        "criteria": [
            "Recent tickets:"
        ]
    },
    {
        "id": "T2-03",
        "account_id": "ACC-3336",
        "criteria": [
            "Recommended TAM Actions"
        ]
    },
    {
        "id": "T2-04",
        "account_id": "ACC-3336",
        "criteria": [
            "Health status:"
        ]
    },
    # Adversarial / incomplete account
    {
        "id": "T2-05-ADV",
        "account_id": "DOES-NOT-EXIST",
        "expect_error": True
    }
]