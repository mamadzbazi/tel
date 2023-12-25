from pyrogram import Client

plugins = dict(root = "plugins")
api_id = 13897640
api_hash = "abe102785a999d41eee2db75b1ec058c"
token = "1084433642:AAFqX-j9SARtCl7rbPvEx918vZnikRpUXgk"
app = Client(name="testbot",api_hash=api_hash,api_id=api_id,bot_token=token,plugins=plugins)


app.run()

