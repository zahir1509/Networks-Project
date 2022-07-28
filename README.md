# Computer Networks Final Project

**Project towards the fulfillment of credits for Computer Networks [CS-1340] | Monsoon 2021 | Ashoka University**

**Python Socket Program with a spam detection model at the server end.**

***

**Steps:**

1. Clone/pull/download this repository
2. Install the virtualenv package with `pip install virtualenv`
3. Navigate to the root directory of this repository in terminal or command prompt and create a virtualenv with `virtualenv env` 
4. Activate the virtualenv with `env\scripts\activate` on Windows OR `source env/bin/activate` on Mac/Linux 
5. Install dependencies with `pip install -r requirements.txt`
6. Run server with `python server.py`
7. Run client with `python client.py`

**Notes:**
- Messages between client and server are encrypted.
- Server is always active and starts looking for a new connection as soon as the previous client window is closed or connection is terminated. 
- Users will need to be authenticated before getting access to the ML model.
- Users will be prompted to enter a username. If the username exists, they will be asked to enter the password to login. If the username does not exist, they will be asked to set a password for registration. 
- After registration/login, users will be prompted to either send a text or a file to the server, to be run through the spam detection model. Users can choose between either option by typing in `text` or `file`.
- If the users choose text, they will be prompted to type in the text, which is sent to the server and processed, and the server returns a text stating if the sent text was spam or not.
- If the users choose file, the file named `input.csv` in the `client` directory will be sent to the server. The server will create a new column in the file, and write whether the text is each row is spam or ham(not spam). The file will then automatically be sent back to the client and saved as `output.csv` in the `client` directory.
- A sample `input.csv` file is already included in the `client` folder, but you can replace that with any other csv file as long as the filename is the same, and all messages to be processed in a single column (different rows).