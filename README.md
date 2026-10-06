# orders-app
<h2>how to run this app?</h2>
<p>1. clone the github repo on your device</p>
<p>2. make sure you have the latest python 3 version installed with its associated venv module and pip package installer</p>
<p>sudo apt install python3 ; sudo apt install python3-venv ; sudo apt install python3-pip</P>
<p>3. create a python venv and activate it, python3 -m venv ./.venv ; source ./.venv/bin/activate</p>
<p>4. install requirements, python3 -m pip install -r requirements.txt</p>
<p>5. navigate into the app directory and run, uvicorn main:app &</p>
<p>6. if server successfully starts then the status can be checked as, curl localhost:8000/health</p>
<p>you should see {"status":"daves hot chicken"}</p>
