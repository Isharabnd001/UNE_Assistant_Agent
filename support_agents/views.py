from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import asyncio
from .agents import triage_agent
from agents import Runner
from openai import RateLimitError
from django.shortcuts import render
import logging
from support_agents.utils.annonymize_filter import anonymize_query
from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    OutputGuardrailTripwireTriggered,
    MaxTurnsExceeded,
    ModelBehaviorError,
    UserError,
    AgentsException
)

#initializing logger to log warnings, errors, info
logger = logging.getLogger(__name__)

@csrf_exempt
def chat_view(request):


    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("message", "")

        #anonymizing the user input query
        anonymized_query = anonymize_query(query)

        logger.info(f"Annonymized Query: {anonymized_query}")

        try:
            #Retrieving previous session id to append to query continuous conversation with history maintained throughout the session
            previous_id = request.session.get("previous_response_id")
            result = asyncio.run(Runner.run(triage_agent, input=query, previous_response_id=previous_id))
 
            #updating previous response id with current response id
            request.session["previous_response_id"] = result.last_response_id
            request.session.modified = True
     
            #succesful return  
            return JsonResponse({
                "response": result.final_output,
                "agent": result.last_agent.name
            })


        #Exception raised when the maximum number of turns is exceeded.
        except MaxTurnsExceeded as e:
            logger.warning(f"Max Turns Exceeded Exception: {str(e)}")
            return JsonResponse({
                "error": "I'm having trouble answering this question clearly. Could you please rephrase or simplify your question?"
            }, status=429)

        #Exception raised when the model does something unexpected
        except ModelBehaviorError as e:
            logger.warning(f"Model Behavior Exception: {e.message}")
            return JsonResponse({
                "error": "Sorry, I ran into a technical issue processing that request. Could you try asking differently?"
            }, status=504)
        
        #Exception raised when the user makes an error using the SDK.
        except UserError as e:
            logger.error(f"User Error: {e.message}")
            return JsonResponse({
                "error": "Oops! Something went wrong on our side while setting up your request. We’re working on it. Please try again soon."
            }, status=501)

        #Exception raised when query contains bad words Eg: Contains banned words like "what the hell"
        except InputGuardrailTripwireTriggered as e:
            logger.warning(f"Guardrail Exception: {str(e)}")
            return JsonResponse({
                "error": "That question can't be processed due to restricted content. Could you try asking differently"
            }, status=405)

        #Agent response filtering Exception : Eg: When agent response is more than 2000 words
        except OutputGuardrailTripwireTriggered as e:
            logger.warning(f"Guardrail Exception: {str(e)}")
            return JsonResponse({
                "error": "The assistant's reply was blocked due to content limsits."
            }, status=406)

        #Base class for all exceptions in the Open AI Agents SDK.
        except AgentsException as e:
            logger.error(f"Agent Exception: {str(e)}")
            return JsonResponse({
                "error": "Oops! Something went wrong on our side while setting up your request. We’re working on it. Please try again soon."
            }, status=503)

        #Unclassified Exception
        except Exception as e:
            logger.error(f"Uncategorized Exception: {str(e)}")
            return JsonResponse({
                "error": "Oops! Something went wrong on our side while setting up your request. We’re working on it. Please try again soon."
            }, status=500)



def home_view(request):
    return render(request, "index.html")


