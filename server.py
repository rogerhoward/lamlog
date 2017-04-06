#!/usr/bin/env python
import os
import StringIO
import flask
import boto3
import config
import simplejson as json
import time


from pprint import pprint

app = flask.Flask(__name__)

    s3 = boto3.resource('s3')

#------------------------------------------------#
#  Bot endpoint                                  #
#------------------------------------------------#

@app.route('/', methods=['POST'])
def log():
    """
    Main route which handles inbound Slack commands.
    """

    # Grab form data from Slack inbound, and pass it to plugin dispatch
    # Payload format documented at https://api.slack.com/slash-commands#how_do_commands_work

    request_data = flask.request.values.to_dict(flat=False)
    print(request_data)

    io = StringIO.StringIO()

    json.dump(request_data, io)

    time_ms = int(round(time.time() * 1000))

    key = '{}.json'.format(time_ms)

    s3.upload_fileobj(io, config.S3_LOG_BUCKET, key)

    response = flask.Response()
    response.status_code = 200
    return response

    

#------------------------------------------------#
# Supporting endpoints                           #
#------------------------------------------------#

@app.route('/info/')
def info():
    """
    Route which returns environmental info as a JSON object.
    """


    return flask.jsonify({'env': config.ENV})


#------------------------------------------------#
#  Command line options                          #
#------------------------------------------------#

def run():
    app.run(processes=3, host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run()
