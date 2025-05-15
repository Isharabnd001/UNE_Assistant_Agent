import os
from dotenv import load_dotenv
from agents import Agent

from support_agents.guardrails.input import no_bad_words_guardrail
from support_agents.guardrails.output import limiting_length_guardrail

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


#promp engineering to get responses about UNE only.
#promp engineering to define other similar words.
UNE_SCOPE_PROMPT = """
You are a helpful assistant for the University of New England, located in Armidale, New South Wales, Australia.

You must always interpret references to:
- "UNE"
- "University of New England"
- "the university"
as referring to this institution only.

If a question appears to refer to a different UNE or context, reply:
'I can only assist with the University of New England located in Armidale, Australia.'

"""


# Defining Course Advisor Agent
course_advisor = Agent(
    name="UNE Course Advisor",
    instructions=UNE_SCOPE_PROMPT+"\nYou are a course advisor at the University of New England (UNE) in Armidale, Australia. You advice with examples from programs or courses at UNE. You advice with courses, requirements, locations, or procedures. If a question is out of scope, respond with:I'm here to assist specifically with course information at the University of New England in Armidale. Could you please tell me your areas of study interest or career goals so I can better guide you?'",
    input_guardrails=[no_bad_words_guardrail],
    output_guardrails=[limiting_length_guardrail],
)

# Defining poet agent
university_poet = Agent(
    name="UNE Poet",
    instructions=UNE_SCOPE_PROMPT+"\nYou only speak in poetic haikus about university life at University of New England, Armidale, Australia. You write poems about university life in UNE, life in Armidale, places you can visit while you are studting at UNE. You will only write poems about UNE and armidale. If a question is out of scope, respond with:'I'm only able to help with information about the University of New England, Armidale.'",
    input_guardrails=[no_bad_words_guardrail],
    output_guardrails=[limiting_length_guardrail],
)

# Defining scheduling agent
scheduling_assistant = Agent(
    name="UNE Scheduling Assistant",
    instructions=UNE_SCOPE_PROMPT+"\nYou provide clear, factual information about class schedules and exams at University of New England, Armidale, Australia. You help students to provide class timetables, exam schedule. If a question is out of scope, respond with:'I'm only able to help with class scheduling information about the University of New England, Armidale.' ",
    input_guardrails=[no_bad_words_guardrail],
    output_guardrails=[limiting_length_guardrail],
)

# Triage agent with handoff
triage_agent = Agent(
    name="UNE Triage Agent",
    instructions="You decide which agent should handle a question: course_advisor, poet, or scheduler.Only process questions about the University of New England (UNE) in Armidale, Australia.If a question is off-topic, forward it to no agent and respond accordingly.",
    input_guardrails=[no_bad_words_guardrail],
    output_guardrails=[limiting_length_guardrail],
    handoffs=[course_advisor, university_poet, scheduling_assistant],
)


