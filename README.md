# dockerhub-to-slack-gateway
Notification gateway between Docker Hub automated builds and Slack.

Inspired by https://github.com/neonadventures/slack-docker-hub-integration which I have used with satisfaction.

Unfortunately there's no direct connection between Docker Hub and Slack to get notifications about automated builds so you have to run your own bridging service. If you don't have your own server or don't feel comfortable running an app 24/7 this AWS based gateway if for you. 

It relies on AWS API Gateway and AWS Lambda so you only have to pay when notifications do happen and the pricing of these services are ridiculous so won't feel anything.

For ease of your I have included an [AWS CloudFormation](https://aws.amazon.com/cloudformation/) template wich can be used to fire up everything needed.

In the end Docker Hub will send the notifications to your stack which will call out to Slack with the correct messages format.

## Usage
* Use the _cloudformation.json_ template to start the stack
* Create a Slack custom integration and grab the URL.
* Grab the API Gateway's URL which should be _https://[random string].execute-api.[region].amazonaws.com/v1/_ and replace _https://hooks.slack.com_ with it in the Slack integration URL.
* Use the new URL as your webhook endpoint in your Docker Hub automated build configuration.
