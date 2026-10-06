# orders-app
<h2>how to run this app?</h2><br>
<p>1. make sure you have the latest python 3.11 version installed with its associated venv module and pip package installer (if not already installed)</p>
<p>sudo apt install python3.11 ; sudo apt install python3.11-venv ; sudo apt install python3.11-pip</P>
<p>2. pull the github repo on your device</p><br>
<p>3. activate the venv, python3.11 -m venv ./.venv ; source ./.venv/bin/activate</p><br>
<p>4. install requirements, python3.11 -m pip install -r requirements.txt</p><br>
<p>5. navigate into the app directory and run, uvicorn main:app &</p><br>
<p>6. if server successfully starts then the status can be checked as, curl localhost:8000/health</p>
