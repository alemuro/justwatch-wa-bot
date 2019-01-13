from justwatch import JustWatch
from twilio.rest import Client
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)


def responseTwilio(f, t, m):
    account = os.environ['TWILIO_ACCESS']
    token = os.environ['TWILIO_SECRET']
    client = Client(account, token)

    call = client.messages.create(to=t, from_=f, body=m)
    return True


def notIn(array, key):
    for obj in array:
        if obj == key:
            return False
    return True


def getPlatforms(offers, stream_platforms, purchase_platforms):
    for x in offers:
        if x["monetization_type"] == "flatrate":
            if notIn(stream_platforms, x['urls']['standard_web']):
                stream_platforms.append(x['urls']['standard_web'])
        if x["monetization_type"] == "buy":
            if notIn(purchase_platforms, x['urls']['standard_web']):
                purchase_platforms.append(x['urls']['standard_web'])
    return True


@app.route("/")
def hello():
    just_watch = JustWatch(country='ES')
    results = just_watch.search_for_item(query="Friends")
    item = results["items"][0]

    stream_platforms = []
    purchase_platforms = []

    platforms = getPlatforms(
        item["offers"], stream_platforms, purchase_platforms)

    # print "--------------------------------------------------"
    # print "- title: %s" % item["title"]
    # print "- original_title: %s" % item["original_title"]
    # print "- original_release_year: %s" % item["original_release_year"]
    # print "- tmdb_popularity: %s" % item["tmdb_popularity"]
    # print "- short_description: %s" % item["short_description"]
    # print "- stream_platforms: %s" % stream_platforms
    # print "- purchase_platforms: %s" % purchase_platforms
    # print "--------------------------------------------------"

    response = ""
    response += "*%s (%s)* \n" % (item["title"], item["original_release_year"])
    response += "\n"
    response += "_%s_ \n" % item["short_description"]
    response += "\n"
    response += "Streaming platforms:\n"
    for url in stream_platforms:
        response += "- %s\n" % url
    response += "\n"
    response += "Purchase platforms:\n"
    for url in purchase_platforms:
        response += "- %s\n" % url

    return jsonify(item)
    # return "Hello!"


@app.route("/query", methods=['POST'])
def query():
    w_from = request.form.get('From')
    w_to = request.form.get('To')
    w_query = request.form.get('Body')
    just_watch = JustWatch(country='ES')
    results = just_watch.search_for_item(query=w_query)
    item = results["items"][0]

    stream_platforms = []
    purchase_platforms = []

    platforms = getPlatforms(
        item["offers"], stream_platforms, purchase_platforms)

    # print "--------------------------------------------------"
    # print "- title: %s" % item["title"]
    # print "- original_title: %s" % item["original_title"]
    # print "- original_release_year: %s" % item["original_release_year"]
    # print "- tmdb_popularity: %s" % item["tmdb_popularity"]
    # print "- short_description: %s" % item["short_description"]
    # print "- stream_platforms: %s" % stream_platforms
    # print "- purchase_platforms: %s" % purchase_platforms
    # print "--------------------------------------------------"

    response = ""
    response += "*%s (%s)* \n" % (item["title"], item["original_release_year"])
    response += "\n"
    response += "%s" % item["short_description"]
    response += "\n"
    response += "Streaming platforms:\n"
    for url in stream_platforms:
        response += "- %s\n" % url
    response += "\n"

    response += "Purchase platforms:\n"
    for url in purchase_platforms:
        response += "- %s\n" % url

    responseTwilio(w_to, w_from, response)

    return "Ok"
