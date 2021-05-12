![duoAlertOxide icon](https://cdn.discordapp.com/attachments/722708774967574618/841409538594570250/g1527.svg.png)

## duoAlertOxide
#### what is it?
duoAlertOxide is a programatic, function-oriented re-implimentation of [duoAlert](https://github.com/Seth-Johnson/duoAlert) by [Seth Johnson](https://gihtub.com/Seth-Johnson), in [rust](https://github.com/rust-lang/rust).

#### what does it do?
duoAlertOxide uses discord webhooks to send a message when a followed user extends or starts a streak based on their daily goal.

<p>&nbsp;</p>
## how do i get this up and running?

#### what does this depend on?
- [rust](https://github.com/rust-lang/rust) (which we'd hope is obvious)

#### building from source
- clone this repository and change into the directory it was cloned in (default duoAlertOxide)
- run `cargo build` to produce a runnable executable (default path `target/debug/<executable>`)
- run the aforementioned executable!*

<sub>* may need additional setup. see [how do i configure this?](#how_do_i_configure_this) </sub>

#### how do i configure this?

DuoAlert reads a basic JSON configuration file to determine which users to follow and what the webhook URL is.  If `use_giphy` is `true` then the phrases pulled from phrases will be used to search giphy and pull the top gif. If `false` your predetermined gifs will be used.

place your `config.json` file in the directory the command is ran from:
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
<p>&nbsp;</p>
## do we have plans for cool stuff?
#### planned features
- multi-hook support
<h6><sub><b><i>are we affiliated at all?</i></b></h6></sub><sub>
We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Duolingo, or any of its subsidiaries or its affiliates. The official Duolingo website can be found at http://duolingo.com. The name “Duolingo” as well as related names, marks, emblems and images are registered trademarks of Duolingo.
</sub>