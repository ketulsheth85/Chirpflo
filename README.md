# InstaChatGPT

1. Install the python enviment and start it.

2. Install Python and Required Library as per requirement.txt file.

3. Config the .env file for initial project setting.

4. Set up database and apply  migrations.

5. Run the python server and celery using below code:
    python : python3 manage.py runserver
    celery : celery -A InstaGpt worker -l INFO