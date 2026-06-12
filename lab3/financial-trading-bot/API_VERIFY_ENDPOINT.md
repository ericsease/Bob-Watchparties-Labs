# Account Verification Endpoint

## Overview

The `/api/account/verify` endpoint tests the exchange connection by signing a test request with the configured API credentials and returns whether authentication succeeds.

## Endpoint Details

- **URL**: `/api/account/verify`
- **Method**: `GET`
- **Authentication**: Uses configured exchange API credentials
- **Content-Type**: `application/json`

## Response

### Success Response (200 OK)

When credentials are valid and authentication succeeds:

```json
{
  "authenticated": true,
  "message": "API credentials verified successfully",
  "signature_valid": true,
  "credentials_present": true,
  "api_key": "abc12345...",
  "timestamp": "2026-06-11T08:00:00.000000+00:00"
}
```

### Failure Response (401 Unauthorized)

When credentials are missing or invalid:

```json
{
  "authenticated": false,
  "message": "Missing API credentials (key, secret, or passphrase)",
  "signature_valid": false,
  "credentials_present": false
}
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `authenticated` | boolean | Whether authentication succeeded |
| `message` | string | Human-readable status message |
| `signature_valid` | boolean | Whether request signature was generated successfully |
| `credentials_present` | boolean | Whether all required credentials are configured |
| `api_key` | string | Partial API key (first 8 chars + "...") for verification |
| `timestamp` | string | ISO 8601 timestamp of verification attempt |

## Usage Examples

### cURL

```bash
curl -X GET http://localhost:5001/api/account/verify
```

### Python (requests)

```python
import requests

response = requests.get("http://localhost:5001/api/account/verify")
result = response.json()

if result["authenticated"]:
    print("✓ Credentials verified successfully")
else:
    print(f"✗ Verification failed: {result['message']}")
```

### JavaScript (fetch)

```javascript
fetch('http://localhost:5001/api/account/verify')
  .then(response => response.json())
  .then(data => {
    if (data.authenticated) {
      console.log('✓ Credentials verified successfully');
    } else {
      console.log(`✗ Verification failed: ${data.message}`);
    }
  });
```

## Configuration

The endpoint uses the following environment variables from `.env`:

- `EXCHANGE_API_KEY` - Your exchange API key
- `EXCHANGE_API_SECRET` - Your exchange API secret
- `EXCHANGE_PASSPHRASE` - Your exchange API passphrase

## Testing

Run the included test script:

```bash
python test_verify_endpoint.py
```

## Use Cases

1. **Health Checks**: Verify exchange connectivity before executing trades
2. **Configuration Validation**: Confirm API credentials are correctly configured
3. **Monitoring**: Periodic checks to ensure credentials haven't expired
4. **Troubleshooting**: Diagnose authentication issues without executing trades

## Security Notes

- The endpoint only returns a partial API key (first 8 characters) for security
- No actual trades or account modifications are performed
- The signature generation process validates credential format and signing capability
- In production, this would make an actual API call to the exchange to verify credentials

## Implementation Details

The verification process:

1. Checks if all required credentials (key, secret, passphrase) are present
2. Generates an HMAC-SHA256 signature for a test request
3. Validates the signature was created successfully
4. Returns authentication status with detailed information

The signature follows standard exchange API patterns:
- Timestamp + Method + Path + Body
- HMAC-SHA256 with API secret
- Headers include: X-API-Key, X-API-Sign, X-API-Timestamp, X-API-Passphrase