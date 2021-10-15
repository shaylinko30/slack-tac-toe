# slack-tac-toe

## Description

This code enables a slack app to render a playable tic-tac-toe game. A slack app will need to be created first and a few configurations will need to be made in order to play the game.  
While the app is running, simply type _/tic-tac-toe_ in a slack _channel_ in order to run the game (make sure that the slack app has been invited to the channel). Multiple games can be played at once.

## Configuration

Follow the instructions on the [slack tutorials page](https://api.slack.com/start/building/bolt-python). The instructions eventually talk about creating/copying an app.py file. Copy the app.py file here instead and then run the python file.

## Future Work

- Create a recursive function for checking for the winner

  - Would it be worth the extra complexity for a small recursion depth?

- Respond to the slack event

- Add some user text to the header in order to log what user pressed the button
