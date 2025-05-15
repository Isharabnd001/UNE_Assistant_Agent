from agents import output_guardrail, GuardrailFunctionOutput
import os
from dotenv import load_dotenv

# loading .env file from root or config directory to access variables
dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(dotenv_path)

#getting the value of MAX_OUTPUT_WORDS from .env file
MAX_OUTPUT_WORDS = int(os.getenv("MAX_OUTPUT_WORDS", "1000"))


# defining a  guardrail to restrict responses above MAX_OUTPUT_WORDS words. Exception will be triggered for responses above 1000 words
@output_guardrail
def limiting_length_guardrail(context, agent, agent_output):
    

    if len(agent_output.split()) > MAX_OUTPUT_WORDS:
        return GuardrailFunctionOutput(
            tripwire_triggered=True,
            output_info={"reason": "Response too long"}
        )
    return GuardrailFunctionOutput(
        tripwire_triggered=False,
        output_info={}
    )
