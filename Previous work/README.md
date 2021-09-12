# SOMs based deep learning model
This repository contains code for a feasibility study of a novel Self-Organising Maps (SOMs) based deep learning framework. It features a web app to easily create, train and visualise the models. Alternatively, the models can be created by directly utilising the backend code.

Directory structure:

- backend/: backend code for creating, training and visualising the SOMs

- frontend/: frontend code for a UI to easily create SOMs

- data/: sample training data that can be used in creating SOMs

- docs/: documents related to the project such as the group contract and project scope

- requirements.txt: a list of dependencies to be installed for the project to run

- server.py: a flask based web server that delivers the front end as well as exposes the backend API


# Accessing the web app online
Web app available at: [https://cp37-soms.herokuapp.com/](https://cp37-soms.herokuapp.com/)

# Running the web app locally
1) Clone the repository

2) Install python3.8+ and gcc-8+

3) Install the dependencies with `pip install -r requirements.txt`

4) Make the cpp bindings with `cd backend && make -j4 && cd ..`

5) Host the web server locally using `gunicorn server:app --access-logfile logfile --limit-request-line 0`
   
   Kill server with `pkill gunicorn`
   
   The following have already been hosted at [https://cp37-soms.herokuapp.com/](https://cp37-soms.herokuapp.com/) but can also be hosted locally. If using the redis and celery worker hosted at [https://cp37-soms.herokuapp.com/](https://cp37-soms.herokuapp.com/), visit the website to boot up the redis and celery workers.
   
   Optional: Instantiate a celery worker in a new terminal with `celery -A server.celery worker`
   
   Optional: Set up a local [redis server](https://redis.io/topics/quickstart) and customise redis_url in celery_worker.py using `redis-server`

# Using the backend SOMs implementation
To use our backend SOM implementation

1) Clone the repository

2) Install python3.8+ and gcc-8+

3) Install the dependencies with `pip install -r requirements.txt`

4) Make the cpp bindings with `cd backend && make -j4 && cd ..`

5) See run_... files for example usage and refer to backend/SOMCpp/doc for documentation on usage