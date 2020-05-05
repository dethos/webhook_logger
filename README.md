# Webhook Logger

**CI Status**: [![CircleCI](https://circleci.com/gh/dethos/webhook_logger.svg?style=svg)](https://circleci.com/gh/dethos/webhook_logger)

This pet project is a simple webhook logger built to test `django-channels`.
It works in a way very similar to [Webhook tester](https://webhook.site).

You create a callback url by visiting the main page, then you use that URL as your webhook callback, all the requests made to it will be displayed on your browser for inspection in real-time.

Feel free to fork, [play with it on the current website](http://webhook-logger.ovalerio.net) or if you prefer launch your own instance (the below button will do it for you without any extra effort).

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/dethos/webhook_logger)

## Setup development environment

To run the project locally you just need to have a machine with `python` and `pipenv` installed then:

1. Install redis-server

2. Copy the sample file with the environment variables:

   > \$ cp .env.sample .env

3. Replace the configuration variables

4. Install the dependencies

   > \$ pipenv install --dev

5. Run the server
   > \$ pipenv run python manage.py runserver

Then the project should be available on: `http://localhost:8000`
