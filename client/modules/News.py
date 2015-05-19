# -*- coding: utf-8-*-
import feedparser
from client import app_utils
import re
from semantic.numbers import NumberService
import sys

WORDS = ["NYHETER", "JA", "NEJ", "FÖRSTA", "ANDRA", "TREDJE"]

PRIORITY = 3

URL = 'http://news.ycombinator.com'


class Article:

    def __init__(self, title, URL):
        self.title = title
        self.URL = URL


def getTopArticles(maxResults=None):
    d = feedparser.parse("http://news.google.se/?output=rss")

    count = 0
    articles = []
    for item in d['items']:
        articles.append(Article(item['title'], item['link'].split("&url=")[1]))
        count += 1
        if maxResults and count > maxResults:
            break

    return articles


def handle(text, mic, profile):
    """
        Responds to user-input, typically speech text, with a summary of
        the day's top news headlines, sending them to the user over email
        if desired.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    mic.say("Ett ögonblick. Hämtar nyheterna.")
    articles = getTopArticles(maxResults=3)
    titles = [" ".join(x.title.split(" - ")[:-1]) for x in articles]
    all_titles = "... ".join(str(idx + 1) + ")" +
                             title for idx, title in enumerate(titles))

    def handleResponse(text):

        def extractOrdinals(text):
            output = []
            service = NumberService()
            for w in text.split():
                if w in service.__ordinals__:
                    output.append(service.__ordinals__[w])
            return [service.parse(w) for w in output]

        chosen_articles = extractOrdinals(text)
        send_all = not chosen_articles and app_utils.isPositive(text)

        if send_all or chosen_articles:
            mic.say("Visst, ge mig en sekund")

            if profile['prefers_email']:
                body = "<ul>"

            def formatArticle(article):
                tiny_url = app_utils.generateTinyURL(article.URL)

                if profile['prefers_email']:
                    return "<li><a href=\'%s\'>%s</a></li>" % (tiny_url,
                                                               article.title)
                else:
                    return article.title + " -- " + tiny_url

            for idx, article in enumerate(articles):
                if send_all or (idx + 1) in chosen_articles:
                    article_link = formatArticle(article)

                    if profile['prefers_email']:
                        body += article_link
                    else:
                        if not app_utils.emailUser(profile, SUBJECT="",
                                                   BODY=article_link):
                            mic.say("Jag har problem att skicka artiklarna. Tyvärr. " +
                                    "Du behöver se till att inställningarna för meddelanden är rätt.")
                            return

            # if prefers email, we send once, at the end
            if profile['prefers_email']:
                body += "</ul>"
                if not app_utils.emailUser(profile,
                                           SUBJECT="Hugo här, dina nyheter",
                                           BODY=body):
                    mic.say("Jag har problem att skicka artiklarna. " +
                            "Se till att dina mail-uppgifter stämmer och " +
                            "att jag kan skicka mail ordentligt.")
                    return

            mic.say("Packat och klart.")

        else:

            mic.say("Okej. Jag skickar inga artiklar.")

    if 'phone_number' in profile:
	
        mic.say("Här är alla toppnyheter.")
	#reload(sys)
	#sys.setdefaultencoding('utf-8')
	print all_titles
	mic.say(all_titles)
	mic.say("Ska jag skicka artiklarna? Om så, vilka?")
        handleResponse(mic.activeListen())

    else:
        mic.say(
            "Här är de senaste nyheterna från världen. " + all_titles)


def isValid(text):
    """
        Returns True if the input is related to the news.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(nyheterna|nyheter)\b', text, re.IGNORECASE))
