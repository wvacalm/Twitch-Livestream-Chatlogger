# Twitch Livestream Chatlogger
- TLC records live chat into .log file
- Before uing TLC, you must register an application on your Twitch developer console, read setup.txt for more information, after reading setup.txt, use TLC by running `python3 main.py`
- TLC creates a client to connect to the IRC channel of your desired livestream, the client will ask for the URL you get redirected to after signing in. Once you enter the URL the client will begin to read and log the chat of your desired livestream. Recorded logs will exist in the log folder.