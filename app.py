import os
import json
from slack_bolt import App
from slack_sdk import WebClient

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

def baseGame():
    return [['-','-','-'], ['-','-','-'], ['-','-','-']]

def threeInRow(board, row, column, row_one, column_one, row_two, column_two):
    if board[row][column] == '-':
        return False
    return board[row][column] == board[row + row_one][column + column_one] and board[row + row_one][column + column_one] == board[row + row_two][column + column_two]


def checkTie(board):
    for row in range(0,3):
        for column in range(0,3):
            if board[row][column] == '-':
                return False
    return True

def checkWinner(board):
    # X X X   - - -   - - -
    # - - -   X X X   - - -
    # - - -   - - -   X X X
    if threeInRow(board, 0, 0, 0, 1, 0, 2) or threeInRow(board, 1, 0, 0, 1, 0, 2) or threeInRow(board, 2, 0, 0, 1, 0, 2):
        return True
    # X - -   - X -   - - X
    # X - -   - X -   - - X
    # X - -   - X -   - - X
    if threeInRow(board, 0, 0, 1, 0, 2, 0) or threeInRow(board, 0, 1, 1, 0, 2, 0) or threeInRow(board, 0, 2, 1, 0, 2, 0):
        return True
    # X - -   - - X
    # - X -   - X -
    # - - X   X - - 
    if threeInRow(board, 0, 0, 1, 1, 2, 2) or threeInRow(board, 0, 2, 1, -1, 2, -2):
        return True
    
    return False

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

def getOpposite(value):
    if value == 'X':
        return 'O'
    return 'X'

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
        game = baseGame()
        buttons = renderButtons(game)
        header = renderHeader('Press a square to begin')
        view=buildView(header, buttons)
        
        meta_data = {
            'end_game': False,
            'game': game,
            'current': 'X'
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
        meta_data = json.loads(body['message']['text'])

        if meta_data['end_game']:
            return

        button = body['actions'][0]['action_id']
        row = button[len(button) - 2]
        column = button[len(button) - 1]
        
        if meta_data['game'][int(row)][int(column)] != '-':
            return
        meta_data['game'][int(row)][int(column)] = meta_data['current']
        meta_data['current'] = getOpposite(meta_data['current'])

        buttons = renderButtons(meta_data['game'])
        header = renderHeader('-- Turn ' + meta_data['current'])

        if checkWinner(meta_data['game']):
            header = renderHeader('Winner '+ getOpposite(meta_data['current']))
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

# Start your app
if __name__ == '__main__':
    app.start(port=int(os.environ.get('PORT', 3000)))
