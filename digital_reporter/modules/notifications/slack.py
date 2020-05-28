class SlackNotifier:
    URL = "https://hooks.slack.com/services/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"

    def send_message_to_slack(self, text):
        from urllib import request, parse
        import json

        post = {"text": "{0}".format(text)}

        try:
            json_data = json.dumps(post)
            req = request.Request(self.URL,
                                  data=json_data.encode('ascii'),
                                  headers={'Content-Type': 'application/json'})
            resp = request.urlopen(req)
        except Exception as em:
            print("EXCEPTION: " + str(em))


if __name__ == "__main__":
    SlackNotifier().send_message_to_slack(
        'Dude, this Slack message is coming from my Python program!')
