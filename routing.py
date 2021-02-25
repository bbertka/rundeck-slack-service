#!/usr/bin/python

from flask import Flask, request, redirect, url_for, send_from_directory, jsonify, Response
import json, os, logging
import cfworker
import psutil
import requests

#---------------------------------------------------------------
#
# app routes: end points for the app's web interfaces
#
#---------------------------------------------------------------
worker = cfworker.cfworker( port=int(os.getenv('PORT')) )
worker.app = Flask(__name__, static_url_path='')

@worker.app.route('/')
def keen_chart():
        return worker.app.send_static_file('index.html')

@worker.app.route('/webhook', methods=['POST'])
def rundeck_webhook():
        token = request.form.get('token', None)  # TODO: validate the token
        command = request.form.get('command', None)
        text = request.form.get('text', None)
        print("Webhook text: %s" % text)
        data = {i.split('=')[0]: i.split('=')[1] for i in text.split(', ') }
        print(data)
        #url = data.get('url')
        url = "https://dev.myrundeck.com/api/38/webhook/cdFlSPxZ5qu7GCue1qUPlw8uUd44s0lt#Slack_Webhook"
        task = data.get('task')
        hostname = data.get('hostname')
        headers = {'content-type': 'application/json'}
        json_data = {"url":url,"task":task,"hostname":hostname}
        r = requests.post(url=url, headers=headers, data=json.dumps(json_data))
        return data

#---------------------------------------------------------------
#
# logging: suppresses some of the annoying Flask output
#
#---------------------------------------------------------------
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

