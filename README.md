# slack-tac-toe

## Description

This code enables a slack app to render a playable tic-tac-toe game. A slack app will need to be created first and a few configurations will need to be made in order to play the game.  
While the app is running, simply type _/tic-tac-toe_ in a slack _channel_ in order to run the game (make sure that the slack app has been invited to the channel). Multiple games can be played at once.

## Configuration

Follow the instructions on the [slack tutorials page](https://api.slack.com/start/building/bolt-python). The instructions eventually talk about creating/copying an app.py file. Add the files from the project folder here instead. The command will still be `python3 app.py` to start the bolt server.

The first player, second player and untouched values are configurable (see game.py).

There are a few tests which can be run with the command `python test_app.py`.

**IMPORTANT NOTE**: To display the display name of the user that last played, make sure that the slack bot has `users:read` permission. `users:read` permission can be added to a slack bot by going to the slack bot page overview and then navigating to OAuth & Permissions -> Scopes -> Add an OAuth Scope. If this is not enabled, make sure that the lines `display_name = getDisplayName(body['user']['id'])` and `header = renderHeader(f'-- Turn {current} ( {display_name} played {previous} )')` in app.py are commented out.

## Future Work

- Respond to the slack event

- Add some user text to the header in order to log what user pressed the button &#9745;
