from __future__ import print_function
from InstagramAPI import InstagramAPI
from time import sleep
import json
import sys
import os
import math

def load_from_json(file):
	try:
		with open(file, 'r') as myfile:
			return json.load(myfile)
	except IOError:
		with open(file, 'w') as myfile:
			json.dump({}, myfile)
		return {}

config = load_from_json('config.json')
username = config['username']
password = config['password']
follower_min = config['followerMin']
keep_verified = config['keepVerified']
whitelist = config['whitelist']
whitelist_all = config['whitelistAll']
delay = config['delay']
width = config['width']

def blockPrint():
	sys.stdout = open(os.devnull, 'w')

def enablePrint():
	sys.stdout = sys.__stdout__

def center(text, spacer=' ', length=width, clear=False, display=True):
	if clear:
		os.system('cls' if os.name == 'nt' else 'clear')
	count = int(math.ceil((length - len(text)) / 2))
	if count > 0:
		if display:
			print(spacer * count + text + spacer * count)
		else:
			return (spacer * count + text + spacer * count)
	else:
		if display:
			print(text)
		else:
			return text

def smart_sleep(delay):
	if delay > 0:
		for a in range(delay, 0, -1):
			print('{}\r'.format(center('Sleeping for {} seconds...'.format(str(a)), display=False)), end='')
			sleep(1)
		center('Sleeping for {} seconds complete!'.format(str(delay)))

def format_whitelist(whitelist):
	try:
		with open(whitelist, 'r') as myfile:
			result = myfile.read().splitlines()
	except IOError:
		result = []
	to_remove = []
	for i in range(0, len(result)):
		try:
			result[i] = int(result[i])
		except ValueError:
			username = result[i]
			print('{}\r'.format(center('Formatting @{}...'.format(username), display=False)), end='')
			try:
				blockPrint()
				api.searchUsername(username)
				result[i] = api.LastJson['user']['pk']
				enablePrint()
				center('Successfully formatted @{}!!'.format(username))
			except KeyError:
				enablePrint()
				if api.LastJson['message'] == 'User not found':
					center('Unable to find @{} on Instagram.'.format(username))
					to_remove.append(username)
				else:
					center('Please increase delay in config.json before proceeding.')
					quit()
			if i != len(result) - 1:
				smart_sleep(delay)
			center(' ')
	for item in to_remove:
		result.remove(item)
	return result

def unfollow(item):
	api.unfollow(item[0])
	if not api.LastJson['friendship_status']['following']:
		center('Successfully unfollowed @{}!!'.format(item[1]))
		return True
	else:
		center('Unable to unfollow @{}.'.format(item[1]))
		return False

center(' ', clear=True)
center('Instagram Unfollower by @DefNotAvg')
center('-', '-')
blockPrint()
api = InstagramAPI(username, password)
if(api.login()):
	enablePrint()
	center('Signed in as @{}'.format(username))
	center('-', '-')
	api.getUserFollowings(api.username_id)
	following = api.LastJson['users']
	if whitelist_all:
		with open(whitelist, 'w') as myfile:
			myfile.write('\n'.join([item['username'] for item in following]))
		if len(following) == 1:
			center('Successfully added {} user to {}!!'.format(str(len(following)), whitelist))
		else:
			center('Successfully added {} users to {}!!'.format(str(len(following)), whitelist))
		quit()
	following = [(item['pk'], item['username'], item['is_verified']) for item in following]
	if len(following) == 1:
		print('{}\r'.format(center('Filtering {} currently followed user...'.format(str(len(following))), display=False)), end='')
	else:
		print('{}\r'.format(center('Filtering {} currently followed users...'.format(str(len(following))), display=False)), end='')
	if follower_min > 0:
		to_unfollow = []
		for item in following:
			api.getUsernameInfo(item[0])
			if keep_verified:
				if api.LastJson['user']['follower_count'] >= follower_min and not item[2]:
					to_unfollow.append(item)
			else:
				if api.LastJson['user']['follower_count'] >= follower_min:
					to_unfollow.append(item)
	else:
		if keep_verified:
			to_unfollow = []
			for item in following:
				if not item[2]:
					to_unfollow.append(item)
		else:
			to_unfollow = following
	if len(following) == 1:
		center('Successfully filtered {} currently followed user!!'.format(str(len(following))))
	else:
		center('Successfully filtered {} currently followed users!!'.format(str(len(following))))
	print('{}\n'.format(center('Formatting {}...'.format(whitelist), display=False)))
	formatted_whitelist = format_whitelist(whitelist)
	with open(whitelist, 'w') as myfile:
		myfile.write('\n'.join([str(item) for item in formatted_whitelist]))
	center('Successfully formatted {}!!'.format(whitelist))
	center(' ', clear=True)
	center('Instagram Unfollower by @DefNotAvg')
	center('-', '-')
	center('Signed in as @{}'.format(username))
	center('-', '-')
	to_unfollow = [item for item in to_unfollow if item[0] not in formatted_whitelist]
	count = 0
	if to_unfollow:
		if len(to_unfollow) == 1:
			center('{} user to unfollow...'.format(str(len(to_unfollow))))
		else:
			center('{} users to unfollow...'.format(str(len(to_unfollow))))
		center(' ')
		for i in range (0, len(to_unfollow)):
			if unfollow(to_unfollow[i]):
				count += 1
			smart_sleep(delay)
			center(' ')
		if count == 1:
			center('Successfully unfollowed {} user!!'.format(str(count)))
		else:
			center('Successfully unfollowed {} users!!'.format(str(count)))
	else:
		center(' ')
		center('No users to unfollow.')
else:
	enablePrint()
	print('Failed to login.')