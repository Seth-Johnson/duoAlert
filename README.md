![duoAlert](https://i.imgur.com/hSL0xKP.png)

# duoAlert

Uses discord webhooks to send a message when a followed user extends or starts a streak based on their daily goal.  


## config 

DuoAlert reads a basic JSON configuration file to determine which users to follow and what the webhook URL is.  

	{
	  "webhook_url": "<webhook_url>",
	  "users": ["exampleUser"],
	  
	}
