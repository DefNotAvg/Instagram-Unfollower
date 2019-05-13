# Instagram Unfollower

A simple program to unfollow users on Instagram.

## Getting Started

Edit config.json to your liking then run main.py.

## config.json

* username - Instagram username
* password - Instagram password
* followerMin - Number of followers a person must have to stay following
* keepVerified - true if you'd like to stay following all verified users, false otherwise
* whitelist - Name of a text file containing a a username or user ID per line to stay following regardless of the above criteria
* delay - Number of seconds to wait between each unfollow
* width - Number of characters to center the program output around

## Prerequisites

* Working on Python 2.7.16 or Python 3.6.8
* [InstagramAPI](https://github.com/LevPasha/Instagram-API-python)

## To-Do

- [ ] Update README with examples