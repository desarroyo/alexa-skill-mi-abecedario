# -*- coding: utf-8 -*-

import logging
import json
import random
import math
import re


from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name, viewport
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective, SpeakItemCommand,
    AutoPageCommand, HighlightMode)

from typing import Dict, Any

SKILL_NAME = "Mi Abecedario"
WELCOME_MESSAGE = ("<speak>Bienvenido a la Skill de Abecedario, aquí podrás aprender palabras, animales, números y más. Solo dime una letra. <break time=\"500ms\"/> Si necesitas ayuda, solo dí: 'Ayuda'. ¿Qué deseas realizar? </speak>")
HELP_MESSAGE = ('''<speak> 
<p>Para empezar a aprender palabras, puedes decir: <break time=\"500ms\"/> </p> 
<p>"Alexa, empieza Mi Abecedario y Dime una palabra con la letra A"</p> 
<p>"Dime un animal con la letra ..."</p> 
<p>"Una palabra con la letra ..."</p> 
<p>etc.</p> 
¿Qué deseas realizar?
</speak>''')
HELP_REPROMPT = "¿Qué deseas realizar?"
STOP_MESSAGE = "Gracias por usar esta skill. ¡Adiós! "
EXCEPTION_MESSAGE = "No entendí muy bien, ¿Qué deseas realizar?"

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def apl_img_title_text(title, text):
    return {
    "json" :"apl_img_title_text.json",
                    "datasources" : {
                    "bodyTemplate1Data": {
                        "type": "object",
                        "objectId": "bt1Sample",
                        "backgroundImage": {
                            "contentDescription": None,
                            "smallSourceUrl": None,
                            "largeSourceUrl": None,
                            "sources": [
                                {
                                    "url": "https://observatoriotecnologico.org.mx/assets/img/alexa/abc_black.jpg",
                                    "size": "small",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                },
                                {
                                    "url": "https://observatoriotecnologico.org.mx/assets/img/alexa/abc_black.jpg",
                                    "size": "large",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                }
                            ]
                        },
                        "title": title,
                        "textContent": {
                            "primaryText": {
                                "type": "PlainText",
                                "text": text
                            }
                        },
                        "logoUrl": "https://observatoriotecnologico.org.mx/assets/img/alexa/abecedario_icon.png"
                    }
                }
            }
            
def apl_animales(title, subtitle, text, img, fuente):
    apl_t1 = "Letras"
    apl_t2 = "Animales"
    apl_hintText = ""
    apl_img_back_small = "https://observatoriotecnologico.org.mx/assets/img/abc_black.png"
    apl_img_back_big = "https://observatoriotecnologico.org.mx/assets/img/abc_black.png"
        
    return {
    "json" :"apl_animales.json",
                    "datasources" : {
                    "bodyTemplate3Data": {
                        "type": "object",
                        "objectId": "bt3Sample",
                        "backgroundImage": {
                            "contentDescription": None,
                            "smallSourceUrl": None,
                            "largeSourceUrl": None,
                            "sources": [
                                {
                                    "url": apl_img_back_small,
                                    "size": "small",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                },
                                {
                                    "url": apl_img_back_big,
                                    "size": "large",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                }
                            ]
                        },
                        "title": 'Letra '+title[:1].upper(),
                        "image": {
                            "contentDescription": None,
                            "smallSourceUrl": None,
                            "largeSourceUrl": None,
                            "sources": [
                                {
                                    "url": img,
                                    "size": "small",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                },
                                {
                                    "url": img,
                                    "size": "large",
                                    "widthPixels": 0,
                                    "heightPixels": 0
                                }
                            ]
                        },
                        "textContent": {
                            "title": {
                                "type": "PlainText",
                                "text": title[:1].upper()
                            },
                            "subtitle": {
                                "type": "PlainText",
                                "text": subtitle
                            },
                            "primaryText": {
                                "type": "PlainText",
                                "text": text
                            },
                            "bulletPoint": {
                                "type": "PlainText",
                                "text": "• "+fuente
                            },
                            "t1": {
                                "type": "PlainText",
                                "text": apl_t1
                            },
                            "t2": {
                                "type": "PlainText",
                                "text": apl_t2
                            }
                        },
                        "logoUrl": "https://d2o906d8ln7ui1.cloudfront.net/images/cheeseskillicon.png",
                        "hintText": apl_hintText
                    }
                }
            }
            
def _load_apl_document(file_path):
    # type: (str) -> Dict[str, Any]
    """Load the apl json document at the path into a dict object."""
    with open(file_path) as f:
        return json.load(f)

# Built-in Intent Handlers
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequest")

        speech = WELCOME_MESSAGE

        apl = apl_img_title_text("Bienvenido", re.sub('<[^<]+>', "",WELCOME_MESSAGE))

        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
                RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
            
        #handler_input.response_builder.speak(speech).ask(speech).set_card(
        #    SimpleCard(SKILL_NAME, speech))
        return handler_input.response_builder.response


class AnimalesLetraIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AnimalesLetraIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("animal_letra")
        
        
        slots = handler_input.request_envelope.request.intent.slots
        
        try:
            letra = str(slots["letra"].resolutions.resolutions_per_authority[0].values[0].value.id)
        except:
            letra = None
            
        
        animal_json = _load_apl_document("animales.json")
        animales_letra = {}
        
        
        for k,v in animal_json.items():
         if k.lower().startswith(letra):
            animales_letra[k] =animal_json[k]
        
        list_animales =  list(animales_letra.keys())
        random.shuffle(list_animales)
        
        animal = animales_letra[list_animales[0]]       #str(slots["animal"].value)
        animal_name = animal["name"]                    #str(slots["animal"].resolutions.resolutions_per_authority[0].values[0].value.name)
        animal_id = list_animales[0]                    #str(slots["animal"].resolutions.resolutions_per_authority[0].values[0].value.id)
        
        
        
        try:
            animal_sound = str(animal["sound"])
        except:
            animal_sound = ""
            
        try:
            animal_img = str(animal["imgs"][0])
        except:
            animal_img = None
            
        animal_text = str(animal["abs"])
        animal_desc = str(animal["des"])

        speech = '''<speak>
<p> '''+animal_name+''' </p>
'''+animal_sound +'''
'''+animal_text+'''.  ¿Qué más deseas realizar?
</speak>'''

        if animal_img is None:
            animal_img = "https://observatoriotecnologico.org.mx/assets/img/alexa/animal_default.JPG"
        apl_img_front_small = animal_img
        apl_img_front_big = animal_img
        
        apl = apl_animales(animal_name, animal_name, animal_text, animal_img, "https://es.wikipedia.org")
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
                RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
        

        return handler_input.response_builder.response


class LetraIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LetraIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("palabra_letra")
        
        
        slots = handler_input.request_envelope.request.intent.slots
        
        try:
            letra = str(slots["letra"].resolutions.resolutions_per_authority[0].values[0].value.id)
        except:
            letra = None
            
        
        palabras_json = _load_apl_document("palabras.json")
        palabra_letra = []
        
        
        for palabra in palabras_json:
            if palabra.lower().startswith(letra):
                palabra_letra.append(palabra)
        
        
        random.shuffle(palabra_letra)
        
        palabra = palabra_letra[0]       #str(slots["palabra"].value)
        palabra_name = palabra_letra[0]                    #str(slots["palabra"].resolutions.resolutions_per_authority[0].values[0].value.name)
        palabra_id = palabra_letra[0]                    #str(slots["palabra"].resolutions.resolutions_per_authority[0].values[0].value.id)
        
        
        
        palabra_sound = ""
            
        palabra_img = "https://lasletras.org/wp-content/uploads/"+letra+".jpg"
            
        palabra_text = palabra_name+ " empieza con la letra "+letra
        palabra_desc = palabra_name+ " empieza con la letra "+letra

        speech = '''<speak>
<p> '''+palabra_name+''' </p>
'''+palabra_sound +'''
'''+palabra_text+'''.  ¿Qué más deseas realizar?
</speak>'''

        if palabra_img is None:
            palabra_img = "https://observatoriotecnologico.org.mx/assets/img/alexa/animal_default.JPG"
        apl_img_front_small = palabra_img
        apl_img_front_big = palabra_img
        
        apl = apl_animales(palabra_name, palabra_name, palabra_text, palabra_img, "https://es.wikipedia.org")
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
                RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
        

        return handler_input.response_builder.response


class AnimalIntentHandler(AbstractRequestHandler):
    """Handler for Device Information Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AnimalIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("animal")
        
        slots = handler_input.request_envelope.request.intent.slots
        animal = str(slots["animal"].value)
        animal_name = str(slots["animal"].resolutions.resolutions_per_authority[0].values[0].value.name)
        animal_id = str(slots["animal"].resolutions.resolutions_per_authority[0].values[0].value.id)
        
        animal_json = _load_apl_document("animales.json")
        try:
            animal_sound = str(animal_json[animal_id]["sound"])
        except:
            animal_sound = ""
            
        try:
            animal_img = str(animal_json[animal_id]["imgs"][0])
        except:
            animal_img = None
            
        animal_text = str(animal_json[animal_id]["abs"])
        animal_desc = str(animal_json[animal_id]["des"])

        speech = '''<speak>
<p> '''+animal_name+''' </p>
'''+animal_sound +'''
'''+animal_text+'''.  ¿Qué más deseas realizar?
</speak>'''

        if animal_img is None:
            animal_img = "https://observatoriotecnologico.org.mx/assets/img/alexa/animal_default.JPG"
        apl_img_front_small = animal_img
        apl_img_front_big = animal_img
        
        
        apl = apl_animales(animal_name, animal_name, animal_text, animal_img, "https://es.wikipedia.org")
        
        if viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_LARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_LANDSCAPE_MEDIUM or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.HUB_ROUND_SMALL or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.TV_LANDSCAPE_XLARGE or viewport.get_viewport_profile(handler_input.request_envelope) == viewport.ViewportProfile.MOBILE_LANDSCAPE_SMALL:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).add_directive(
                RenderDocumentDirective(document=_load_apl_document(apl["json"]),datasources=apl["datasources"])
            ).set_should_end_session(False)
        else:
            handler_input.response_builder.speak(speech).ask(HELP_REPROMPT).set_card(SimpleCard(SKILL_NAME, re.sub('<[^<]+>', "",speech))).set_should_end_session(False)
        

        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ( is_intent_name("AMAZON.HelpIntent")(handler_input) or
                is_intent_name("ayuda")(handler_input) )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, re.sub('<[^<]+>', "",HELP_MESSAGE))).set_should_end_session(False)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input) or
                is_intent_name("salir")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE).set_should_end_session(True)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(AnimalesLetraIntentHandler())
sb.add_request_handler(AnimalIntentHandler())
sb.add_request_handler(LetraIntentHandler())
#AnimalesLetraIntent

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
