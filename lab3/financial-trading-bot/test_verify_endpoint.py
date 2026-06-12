#!/usr/bin/env python3
"""Test script for the /api/account/verify endpoint."""

import requests
import json

BASE_URL = "http://localhost:5001"


def test_verify_endpoint():
    """Test the account verification endpoint."""
    print("Testing /api/account/verify endpoint...")
    print("-" * 60)

    try:
        response = requests.get(f"{BASE_URL}/api/account/verify", timeout=5)

        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(response.json(), indent=2))

        if response.status_code == 200:
            print("\n✓ Authentication successful!")
        elif response.status_code == 401:
            print("\n✗ Authentication failed - check your credentials")
        else:
            print(f"\n? Unexpected status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("✗ Error: Could not connect to the server.")
        print("  Make sure the Flask app is running on port 5001")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    test_verify_endpoint()

# Made with Bob
