# -*- coding: utf-8-*-
import datetime
import re
import os
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["T\xc4ND", "SL\xc4CK","SL\xc4CKT","SL\xc4KT", "BELYSNING", "BELYSNINGEN", "LAMPOR", "LAMPORNA"]


def handle(text, mic, profile):
    """
        TODO: Fetch openhab settings from profile.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    mic.say("Jag ska försöka...")
    baseaction = """curl --header "Content-Type: text/plain" --request POST --data """
    action = '"OFF"'
    sayAction = "Släcker"
    if bool(re.search(ur'\bt\xc4nd|p\xc3\b', text, re.IGNORECASE)):
        action = '"ON"'
        sayAction = "Tänder"
    baseaction += action
    
    if bool(re.search(ur'\balla|lampor\b', text, re.IGNORECASE)):
        mic.say("Okej. " + sayAction + " alla lampor.")
        os.system(baseaction + """ http://10.1.1.136:8080/rest/items/Lights/""")
        """ släcker allt """
    elif bool(re.search(ur'\bk\xd6k|k\xd6ket|k\xd6kslampor\b',text, re.IGNORECASE)):
        mic.say("Javisst. Jag " + sayAction + " i köket.")
        os.system(baseaction + """ http://10.1.1.136:8080/rest/items/Kitchen/""")
        """" släcker köket """
    elif bool(re.search(ur'\bvardagsrum|vardagsrummet\b', text, re.IGNORECASE)):
        mic.say("Japp. " + sayAction + " i vardagsrummet")
        os.system(baseaction + """ http://10.1.1.136:8080/rest/items/Livingroom_Window_Light/""")
        os.system(baseaction + """ http://10.1.1.136:8080/rest/items/Livingroom_Ceiling_Window/""")
        os.system(baseaction + """ http://10.1.1.136:8080/rest/items/Livingroom_Ceiling/""")
        os.system(baseaction + """ http://10.1.1.136:8080/rest/items/Livingroom_Aquarium/""")
        """ släcker vardagsrum """

def isValid(text):
    """
        Returns True if input is related to the time.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(ur'\bt\xc4nd|p\xc3|sl\xc4ckt|sl\xc4ck|sl\xc4kt|belysning|belysningen|lampor|lamporna\b', text, re.IGNORECASE))
