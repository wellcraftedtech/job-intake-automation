# Job Extraction Schema & Business Rules

## 1. Fields to Extract

| Field Name | Type | Description |
|------------|------|-------------|
| `client_name` | String | Name of the law firm or company requesting the service. |
| `matter_number` | String | Case reference number (e.g., "2025/1123", "Ref 88291"). Null if not found. |
| `job_type` | enum | One of: `Court Filing`, `Process Service`, `Occupancy Check`, `Enforcement`, `Lockout`, `Field Call`, `Other`. |
| `service_address` | Object | structured address: `{ "street": "...", "suburb": "...", "state": "...", "postcode": "..." }`. |
| `defendant_name` | String | Name of person/entity to be served or checked. |
| `due_date` | Date | Desired completion date in DD/MM/YYYY format. |
| `special_instructions` | String | Any specific constraints (e.g., "attend between 5pm-7pm"). |
| `urgency` | enum | `Normal` or `Urgent`. (Urgent if "urgent", "asap", "rush" mentioned or due <48h). |
| `attachments_mentioned` | Integer| Count of attached documents mentioned in text. |
| `requires_quote` | Boolean | True if the sender specifically asks for a quote/cost. |
| `complexity` | enum | `Low`, `Medium`, `High`. Based on multiple parties, strict conditions, or difficult targets. |

## 2. JSON Output Template

```json
{
  "job_details": {
    "client_name": "Jenkins & Co Lawyers",
    "matter_number": "2025/1123",
    "job_type": "Process Service",
    "service_address": {
      "street": "15 George St",
      "suburb": "Parramatta",
      "state": "NSW",
      "postcode": "2150"
    },
    "defendant_name": "Mr. John Smith",
    "due_date": "06/01/2026",
    "special_instructions": "Individual is known to be aggressive. Attend between 5pm-7pm.",
    "urgency": "Urgent",
    "attachments_mentioned": 1,
    "requires_quote": false,
    "complexity": "Medium"
  }
}
```

## 3. Auto-Quoting Business Rules

| Rule | Base Cost ($AUD) | Notes |
|------|-----------------|-------|
| **Court Filing** | $150 | Standard filing fee. |
| **Process Service** | $120 | Standard metro service (within 25km). |
| **Occupancy Check** | $180 | Includes report and photos. |
| **Field Call** | $150 | Standard debt collection visit. |
| **Enforcement/Lockout**| $350 | Requires senior agent + time on site. |
| **Other** | $0 | Requires manual quote. |

### Surcharges:
*   **Urgent**: +50% of Base Cost.
*   **Regional** (Outside Metro): +$80 flat fee (Simplified rule: if postcode is not strictly 2000-2200 or 3000-3200, assume Regional/Extended).
*   **Multiple Addresses/Parties**: +$80 per additional party/address.
*   **Complexity High**: +$100 flat fee.

### Calculation Logic:
`Total = (Base_Cost * Urgency_Multiplier) + Surcharges`

Example:
*   Job: Process Service ($120)
*   Urgency: Urgent (1.5x)
*   Result: $180
