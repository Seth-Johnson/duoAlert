![duoAlert](https://i.imgur.com/hSL0xKP.png)

# duoAlert

Uses discord webhooks to send a message when a followed user extends or starts a streak in a specifed language.  


## config 

DuoAlert reads a basic JSON configuration file to determine which users to follow, what the webhook URL is, and what language to track.  

	{
	  "webhook_url": "<webhook_url>",
	  "users": ["exampleUser"],
	  "language": "eo"
	}
