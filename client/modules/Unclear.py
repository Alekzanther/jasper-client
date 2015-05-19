# -*- coding: utf-8-*-
from sys import maxint
import random

WORDS = []

PRIORITY = -(maxint + 1)


def handle(text, mic, profile):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    messages = ["Ojsan, skulle du kunna säga det igen?",
                "Jag ber om ursäkt. Skulle du kunna prova igen?",
                "Kan du upprepa det?", "Ursäkta mig?"]

    message = random.choice(messages)

    mic.say(message)


def isValid(text):
    return True
