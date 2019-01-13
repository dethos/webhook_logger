# Webhook Logger

This pet project is a simple webhook logger built to test `django-channels`.
It works in a way very similar to [Webhook tester](https://webhook.site).

Feel free to fork and play with it.

# Setup development environment

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
