from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, AsyncMock
from agents.exceptions import (
    MaxTurnsExceeded,
    ModelBehaviorError,
    UserError,
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    AgentsException,
)
from unittest.mock import MagicMock
from agents import GuardrailFunctionOutput
from agents import GuardrailFunctionOutput

#this class contains unit test cases 
# you can run these unit test cases using command : python manage.py test support_agents.tests

class ChatViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("chat_view") 

    #succesful response unit test case
    @patch("support_agents.views.Runner.run", new_callable=AsyncMock)
    def test_chat_view_success(self, mock_run):
        class FakeAgent:
            name = "UNE Course Advisor"

        class FakeRunResult:
            final_output = "Here are the available courses."
            last_response_id = "mock-id-123"
            agent = FakeAgent()
            last_agent = FakeAgent()
           

        mock_run.return_value = FakeRunResult()

        response = self.client.post(
            reverse("chat_view"),
            data={"message": "What are the available courses?"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["response"], "Here are the available courses.")


    #Bad language restriction test case
    @patch("support_agents.views.Runner.run")
    def test_guardrail_bad_word_input(self, mock_run):
        mock_guardrail = MagicMock()
        mock_guardrail.__class__.__name__ = "NoBadWordsGuardrail"

        guardrail_result = GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info={"reason": "Detected bad word"}
        )
        guardrail_result.guardrail = mock_guardrail  

        mock_run.side_effect = InputGuardrailTripwireTriggered(guardrail_result)

        response = self.client.post(self.url, {"message": "what the hell"}, content_type="application/json")
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())



    #Server Error : Uncategorized error
    @patch("support_agents.views.Runner.run", side_effect=Exception("Something went wrong"))
    def test_chat_view_uncaught_error(self, mock_run):
        response = self.client.post(
            reverse("chat_view"),
            data={"message": "Trigger error"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", response.json())

    #MaxTurnsExceeded Exception test case
    @patch("support_agents.views.Runner.run")
    def test_chat_view_max_turns_exceeded(self, mock_run):
        mock_run.side_effect = MaxTurnsExceeded("Too many turns")

        response = self.client.post(
            self.url,
            data={"message": "Repeat this again and again"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 429)
        self.assertIn("error", response.json())
        self.assertIn("trouble", response.json()["error"].lower())

    #Model behavior error  test case
    @patch("support_agents.views.Runner.run")
    def test_chat_view_model_behavior_error(self, mock_run):
        mock_run.side_effect = ModelBehaviorError("Malformed JSON")

        response = self.client.post(
            self.url,
            data={"message": "Give me something strange"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 504)
        self.assertIn("error", response.json())
        self.assertIn("technical", response.json()["error"].lower())

    #user error test case 
    @patch("support_agents.views.Runner.run")
    def test_chat_view_user_error(self, mock_run):
        mock_run.side_effect = UserError("Configuration error")

        response = self.client.post(
            self.url,
            data={"message": "Tell me something"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 501)
        self.assertIn("error", response.json())
        self.assertIn("working", response.json()["error"].lower())

    # agents exception: base error from open ai agents sdk
    @patch("support_agents.views.Runner.run")
    def test_chat_view_agents_exception(self, mock_run):
        mock_run.side_effect = AgentsException("Generic agent issue")

        response = self.client.post(
            self.url,
            data={"message": "Confuse the agent"},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 503)
        self.assertIn("error", response.json())
        self.assertIn("working", response.json()["error"].lower())

  