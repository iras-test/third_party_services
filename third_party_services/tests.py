import json
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from third_party_services.serializers import ObrsBrnDetailsSerializer


def mock_response(status_code, payload):
    response = Mock()
    response.status = status_code
    response.data = json.dumps(payload).encode("utf-8")
    response.headers = {"Content-Type": "application/json"}
    return response


class ObrsBrnDetailsSerializerTests(SimpleTestCase):
    @patch("third_party_services.serializers.validate_obrs_brn")
    def test_denies_company_statuses_marked_do_not_offer_service(self, validate):
        denied_statuses = {
            "Dormant": "currently dormant",
            "Struck-off": "apply for restoration at URSB",
            "Dissolved/Ceased": "dissolved or ceased operations",
            "De_Registered": "deregistered",
            "In_Provisional_liquidation": "under provisional liquidation",
            "In_Liquidation": "undergoing liquidation",
        }

        for registration_status, expected_message_part in denied_statuses.items():
            with self.subTest(registration_status=registration_status):
                validate.return_value = mock_response(
                    200,
                    {
                        "data": {
                            "entityName": "EXAMPLE COMPANY LIMITED",
                            "registrationStatus": registration_status,
                        },
                        "status": 200,
                    },
                )

                payload, response_status = ObrsBrnDetailsSerializer(
                    data={"brn": "80034888173303"}
                ).details()

                self.assertEqual(response_status, 400)
                self.assertEqual(payload["error"], "OBRS_SERVICE_NOT_ALLOWED")
                self.assertTrue(payload["detail"].startswith("EXAMPLE COMPANY LIMITED"))
                self.assertIn(expected_message_part, payload["detail"])
                self.assertNotIn("entityName", payload)
                self.assertEqual(payload["data"]["legal_name"], "")

    @patch("third_party_services.serializers.validate_obrs_brn")
    def test_returns_company_for_registered_status(self, validate):
        validate.return_value = mock_response(
            200,
            {
                "data": {
                    "entityName": "EXAMPLE COMPANY LIMITED",
                    "incorporationDate": "2026-02-15",
                    "registrationStatus": "Registered",
                },
                "status": 200,
            },
        )

        payload, response_status = ObrsBrnDetailsSerializer(
            data={"brn": "80034888173303"}
        ).details()

        self.assertEqual(response_status, 200)
        self.assertEqual(payload["entityName"], "EXAMPLE COMPANY LIMITED")
        self.assertTrue(payload["isValid"])

    @patch("third_party_services.serializers.validate_obrs_brn")
    def test_preserves_service_status_error(self, validate):
        service_error = {
            "error": "OBRS_SERVICE_NOT_ALLOWED",
            "message": "This company is currently dormant.",
            "detail": "This company is currently dormant.",
            "data": {"registrationStatus": "Dormant"},
            "status": 400,
        }
        validate.return_value = mock_response(400, service_error)

        payload, response_status = ObrsBrnDetailsSerializer(
            data={"brn": "80034888173303"}
        ).details()

        self.assertEqual(response_status, 400)
        self.assertEqual(payload, service_error)
