![duoAlert](https://i.imgur.com/hSL0xKP.png)

# duoAlert

Uses discord webhooks to send a message when a followed user extends or starts a streak based on their daily goal.  


## config

DuoAlert reads a basic JSON configuration file to determine which users to follow and what the webhook URL is.  If `use_giphy` is `true` then the phrases pulled from phrases will be used to search giphy and pull the top gif. If `false` your predetermined gif's will be used.

	{
	  "username":"<username_of_duolingo>",
	  "password":"<password_of_duolingo>",
	  "webhook_url": "<discord_webhook_url>",
	  "users": ["exampleUser"],
	  "use_giphy": true,
	  "giphy_rating": "G",
	  "giphy_apikey": "YOUR_API_KEY_HERE",
	  "sadness_gif": "https://media.giphy.com/media/Ty9Sg8oHghPWg/giphy.gif",
	  "sadness_phrase": "Sadness"
	}

## Notice of Non-Affiliation and Disclaimer 

We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Duolingo, or any of its subsidiaries or its affiliates. The official Duolingo website can be found at http://duolingo.com. The name “Duolingo” as well as related names, marks, emblems and images are registered trademarks of Duolingo.
