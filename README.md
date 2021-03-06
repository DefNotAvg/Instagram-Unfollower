# Instagram Unfollower

A simple program to unfollow users on Instagram.

## Getting Started

Edit config.json to your liking then run main.py.

## config.json

* username - Instagram username
* password - Instagram password
* removeUnfollowers - true if you'd like to remove only users that don't follow you, false otherwise
* keepVerified - true if you'd like to stay following all verified users regardless if they follow you, false otherwise
* whitelist - Name of a text file containing a username or user ID per line to stay following regardless of the above criteria
* whitelistAll - true if you'd like to add all currently followed users to the whitelist before beginning, false otherwise (must be set to false to begin the unfollowing process)
* delay - Number of seconds to wait between each API action
* width - Number of characters to center the program output around

## Prerequisites

* Working on Python 2.7.16 or Python 3.6.8
* [InstagramAPI](https://github.com/LevPasha/Instagram-API-python)

## To-Do

- [ ] Add ability to easily remove users from whitelist
- [ ] Update README with examples