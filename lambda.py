import json
import urllib2


def docker_callback(url, payload):
    docker_request = urllib2.Request(
        url,
        json.dumps(payload),
        {'Content-Type': 'application/json'})

    try:
        urllib2.urlopen(docker_request)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to reach ', url
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code

        return e

    return 'success'


def handler(event, context):
    slack_url = "https://hooks.slack.com%s" % event['path']
    incoming = json.loads(event['body'])
    docker_callback_url = incoming['callback_url']

    payload = {
        'text': "[<%s|%s>] new image build complete with tag %s"
        % (incoming['repository']['repo_url'],
            incoming['repository']['repo_name'],
            incoming['push_data']['tag'])
    }

    slack_request = urllib2.Request(
        slack_url,
        json.dumps(payload),
        {'Content-Type': 'application/json'})

    try:
        urllib2.urlopen(slack_request)
    except urllib2.URLError as e:
        docker_callback(
            docker_callback_url,
            {'state': 'error'}
        )

        if hasattr(e, 'reason'):
            print 'We failed to reach ', slack_url
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code

        return {
            'statusCode': e.code,
            'body': e.reason
        }

    response = docker_callback(
        docker_callback_url,
        {'state': 'success'}
    )

    if response == 'success':
        return {
            'statusCode': 200,
            'body': 'success'
        }
    else:
        return {
            'statusCode': response.code,
            'body': response.reason
        }
