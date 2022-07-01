import os
import json
from slack_bolt import App
from slack_sdk import WebClient

from game import *

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)
client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))

index_to_tic = {
    0: '00',
    1: '01',
    2: '02',
    3: '10',
    4: '11',
    5: '12',
    6: '20',
    7: '21',
    8: '22'
}

def renderHeader(text):
    return {
        'type': 'header',
        'text': {
            'type': 'plain_text',
            'text': text,
            'emoji': True
        }
    }

def renderButtons(game):
    buttons = []
    for row in range(0,3):
        for column in range(0,3):
            text = game[row][column]
            buttons.append({
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': text
                },
                'value': str(row)+str(column),
                'action_id': 'button_'+str(row)+str(column)
            })
    return buttons

def buildView(header, buttons):
    return {
        'callback_id': 'tic_tac_toe',

        # body of the view
        'blocks': [
            header,
            {
                'type': 'actions',
                'block_id': 'row0',
                'elements': buttons[0:3]
            },
            {
                'type': 'actions',
                'block_id': 'row1',
                'elements': buttons[3:6]
            },
            {
                'type': 'actions',
                'block_id': 'row2',
                'elements': buttons[6:9]
            }
        ]
      }

# Home Tab
@app.event('app_home_opened')
def updateHomeTab(client, event, logger):
  try:
    client.views_publish(
      user_id=event['user'],
      view={
        'type': 'home',
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': 'Welcome to *Tic-Tac-Toe*!  \nInvite me to a channel and type */tic-tac-toe* to start a game.'
                }
            }
        ]
      }
    )
  
  except Exception as e:
    logger.error(f'Error publishing home tab: {e}')

#Slash Command
@app.command('/tic-tac-toe')
def slashCommand(ack, respond, command):
    ack()
    try:
        game = getBaseGame()
        buttons = renderButtons(game)
        header = renderHeader('Press a square to begin')
        view=buildView(header, buttons)
        
        meta_data = {
            'end_game': False,
            'game': game,
            'current': firstPlayerValue
        }

        meta_data_text = json.dumps(meta_data)

        global client
        client.chat_postMessage(
            channel = command['channel_id'],
            text = meta_data_text,
            blocks = view['blocks']
        )
        # respond to the call

    except Exception as e:
        print(f'Error with slack_command: {e}')

# Button Events
for index in range(0,9):
    @app.action('button_'+ index_to_tic[index])
    def buttonPressed(ack, body, client):
        ack()
        print(body['user']['id'])
        # Must have users:read permission to use this, see note in README
        display_name = getDisplayName(body['user']['id'])
        meta_data = json.loads(body['message']['text'])

        # Do not change anything after the game has ended
        if meta_data['end_game']:
            return

        # The button stores which row and column was pressed
        # button_01 means 0 is the row and 1 is the column
        button = body['actions'][0]['action_id']
        row = button[len(button) - 2]
        column = button[len(button) - 1]
        
        # If the button already has a value do not change the button
        if meta_data['game'][int(row)][int(column)] != untouchedValue:
            return
        # Update the button from untouchedValue to current and update current
        previous = meta_data['current']
        current = getOpposite(meta_data['current'])
        meta_data['game'][int(row)][int(column)] = previous
        meta_data['current'] = current

        # Render the buttons and header with the new game data
        buttons = renderButtons(meta_data['game'])
        header = renderHeader(f'-- Turn {current} ( {display_name} played {previous} )')
        # header = renderHeader(f'-- Turn {current}')

        if checkWinner(meta_data['game']):
            header = renderHeader('Winner '+ previous)
            meta_data['end_game'] = True

        if checkTie(meta_data['game']):
            header = renderHeader('Tie')
            meta_data['end_game'] = True
            
        view=buildView(header, buttons)
            
        try:
            client.chat_update(
                channel = body['channel']['id'],
                ts = body['message']['ts'],
                as_user = True,
                text = json.dumps(meta_data),
                blocks = view['blocks']
            )
        except Exception as e:
            print(f'Error with button press: ' + button)
            print(e)

def getDisplayName(user_id):
    try:
    # Call the users.info method using the WebClient
        result = client.users_info(
            user=user_id
        )
        return result['user']['profile']['display_name']

    except Exception as e:
            print(f'Error getting display_name for: ' + user_id)
            print(e)

# Start your app
if __name__ == '__main__':
    app.start(port=int(os.environ.get('PORT', 3000)))
