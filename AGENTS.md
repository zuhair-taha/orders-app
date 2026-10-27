project's root directory: orders-app

How to run the project?
    - first activate the venv from the root directory by running "source ./.venv/bin/activate", if there is no .venv file, then first install python 3.11 and create the venv by "running python3.11 -m venv .venv". Next activate the venv.
    - inatall all the requirements by running "python -m pip install -r requirements.txt"
    - run the app by running command in the /app directory, "uvicorn main:app"
How to run the tests?
    - make sure you have activated the venv and installed all the requirements
    - in the /app directory run pytest test_main.py
The rules:
    - Always store and compute money as integer cents. Never use floats.
    - Always use ? placeholders in SQL. Never build queries with f-strings or string formatting.
    - Always log every request as one JSON line with method, path, status code and duration in ms
    - Every test in the test_main.py file should use a "tmp_path" to create a orders.db from environment variable "ORDERS_DB"
