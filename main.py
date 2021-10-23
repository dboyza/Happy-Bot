import os, discord, requests, json, random
from replit import db

client = discord.Client();

sad_words = ['depressed', 'sad', 'not happy', 'angry', 'depressing', 'crying', 'im done']

starter_encouragements = [
  'It will get better!', 
  'Cheer up!', 
  'Hang in there!'
]

if 'responding' not in db.keys():
  db['responding'] = True

# Get a random quote from the Zenquotes api
# How: Turn response from API into json, retur concatenated quote and author
def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return quote

# Update the database with a new encouraging message
def update_encouragements(encouraging_message):
  if 'encouragements' in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]

# Delete an encouraging message from the database
def delete_encouragement(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
  db['encouragements'] = encouragements

# Prints login when bot starts running
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

# Interactions with discord server messages
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # Gets info from user message
  msg = message.content

  # Get quote from API
  if msg.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  # Commands (if responding)
  if db['responding']:
    options = starter_encouragements
    if 'encouragements' in db.keys():
      options = options + db['encouragements'].value

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  # NEW command
  if msg.startswith('!new'):
    encouraging_message = msg.split('!new ', 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send('New encouraging message "{0}" added.'.format(encouraging_message))
  
  # DEL command
  if msg.startswith('!del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('!del',1)[1])
      delete_encouragement(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  # LIST command
  if msg.startswith('!list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  #REPSONDING command
  if msg.startswith('!responding'):
    value = msg.split('!responding ', 1)[1]
    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Repsonding: ON')
    else:
      db['responding'] = False
      await message.channel.send('Repsonding: OFF')


# Run the bot
my_secret = os.environ['bot_token']

client.run(os.getenv('bot_token'))