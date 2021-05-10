![duoAlertOxide icon](https://cdn.discordapp.com/attachments/683096422362775574/841364917525544990/68747470733a2f2f692e696d6775722e636f6d2f68534c30784b502e706e67-NEW.png)

# duoAlertOxide

Uses discord webhooks to send a message when a followed user extends or starts a streak based on their daily goal.
 
Rust re-implimentation of [Seth Johnson's duoAlert](https://github.com/seth-johnson/duoAlert)

## config

DuoAlert reads a basic JSON configuration file to determine which users to follow and what the webhook URL is.  If `use_giphy` is `true` then the phrases pulled from phrases will be used to search giphy and pull the top gif. If `false` your predetermined gif's will be used.

in the directory the command is ran from:
```
config.json
--------------------------------
```

```json
	{
	  "username":"<username_of_duolingo>",
  	  "password":"<password_of_duolingo>",
	  "webhook_url": "<webhook_url>",
	  "users": ["exampleUser"],
	  "use_giphy": true,
          "giphy_apikey": "YOUR_API_KEY_HERE",
          "giphy_rating": "G"
	}
```

## Notice of Non-Affiliation and Disclaimer 

We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Duolingo, or any of its subsidiaries or its affiliates. The official Duolingo website can be found at http://duolingo.com. The name “Duolingo” as well as related names, marks, emblems and images are registered trademarks of Duolingo.
