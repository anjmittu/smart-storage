# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

import boto3
import random
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BASE_URL = "http://72.83.3.43/"


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can store or retrieve an item. Which would you like to try?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CloseBoxIntentHandler(AbstractRequestHandler):
    """Handler for Retrieve Item Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CloseBoxIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        try:
            requests.get(BASE_URL+"close/1")
        except:
            # The client doesn't return a valid response so we will catch and move on
            pass
        speak_output = "Closing the box"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class RetrieveItemIntentHandler(AbstractRequestHandler):
    """Handler for Retrieve Item Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RetrieveItemIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        item_to_store = handler_input.request_envelope.request.intent.slots['box_item'].value
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('a12d15a7-b62a-4d77-90c8-40b63c3ddefe')
        response = table.get_item(Key={'id': item_to_store})
        
        if "Item" in response:
            box_id = response['Item']["box_id"]
            try:
                requests.get(BASE_URL+"open/"+str(box_id))
            except:
                # The client doesn't return a valid response so we will catch and move on
                pass
            speak_output = "Get the {} in box {}. Tell me when to close the box.".format(item_to_store, box_id)
        else:
            speak_output = "There was a problem getting the item"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class StoreItemIntentHandler(AbstractRequestHandler):
    """Handler for Store Item Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("StoreItemIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        item_to_store = handler_input.request_envelope.request.intent.slots['storage_item'].value
        box_id = int(round(random.uniform(1, 2)))
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('a12d15a7-b62a-4d77-90c8-40b63c3ddefe')
        response = table.put_item(
           Item={
                "id": item_to_store,
                "box_id": box_id
            }
        )
        
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            try:
                requests.get(BASE_URL+"open/"+str(box_id))
            except:
                # The client doesn't return a valid response so we will catch and move on
                pass
            speak_output = "Store the {} in box {}.  Tell me when to close the box.".format(item_to_store, box_id)
        else:
            speak_output = "There was a problem storing the item"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "For example, if you want to store a pen say, i want to store a pen in my box."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CloseBoxIntentHandler())
sb.add_request_handler(RetrieveItemIntentHandler())
sb.add_request_handler(StoreItemIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()