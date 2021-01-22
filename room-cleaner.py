import discord
import os
import configargparse
import signal

print("starting.....")

defaultconfigfiles = [os.getenv('servAP_CONFIG', os.path.join(os.path.dirname(__file__), './room-config.ini'))]
parser = configargparse.ArgParser(default_config_files=defaultconfigfiles,auto_env_var_prefix='servAP_',description='Database')
parser.add_argument('--token', help='Discord Bot Token', required=True)
parser.add_argument('--nest-channel', help='Channel ID to post into', type=int, required=True)

options = parser.parse_args()

print(options)

def is_me(m):
    return m.author == client.user

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))
        print("starting main...")
        # await client.wait_until_ready()
        print(options.nest_channel)
        channel = client.get_channel(options.nest_channel)
        print("Using Channel")
        print(channel)
        print(str(channel.last_message_id))
        if isinstance(channel.last_message_id, int) and channel.last_message_id > 0:
            delete = await channel.purge(limit=200, bulk=True)
            print("purged {} messages".format(str(len(delete))))
        client.clear()
        try:
            os.kill(os.getpid(),signal.SIGKILL)
            # await client.close()
        except discord.HTTPException as err:
            print(err)
            pass
        print ("done!")
        exit(0)

client = MyClient()
client.run(options.token)
