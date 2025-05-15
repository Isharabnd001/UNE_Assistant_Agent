from agents import input_guardrail,GuardrailFunctionOutput
from support_agents.utils.load_bad_words import load_bad_words

#loading bad words from bad_words.txt file
BAD_WORDS = load_bad_words()

@input_guardrail
def no_bad_words_guardrail(context, agent, text):

    
    for word in BAD_WORDS:
        if word in text.lower():
            return GuardrailFunctionOutput(
                tripwire_triggered=True,
                output_info={"reason": f"Blocked word: {word}"}
            )
    return GuardrailFunctionOutput(tripwire_triggered=False, output_info={})
