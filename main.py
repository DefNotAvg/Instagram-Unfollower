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
keep_verified = config['keepVerified']
remove_unfollowers = config['removeUnfollowers']
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

def header(full=True):
	center(' ', clear=True)
	center('Instagram Unfollower by @DefNotAvg')
	center('-', '-')
	if full:
		center('Signed in as @{}'.format(username))
		center('-', '-')

def smart_sleep(delay):
	if delay > 0:
		for a in range(delay, 0, -1):
			print('{}\r'.format(center('Sleeping for {} seconds...'.format(str(a)), display=False)), end='')
			sleep(1)
		center('Sleeping for {} seconds complete!'.format(str(delay)))

def format_whitelist(whitelist):
	center('Formatting {}...'.format(whitelist))
	center(' ')
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
				api_result = api.LastJson
				result[i] = api_result['user']['pk']
				enablePrint()
				center('Successfully formatted @{}!!'.format(username))
			except KeyError:
				enablePrint()
				if api_result['message'] == 'User not found':
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
	with open(whitelist, 'w') as myfile:
		myfile.write('\n'.join([str(item) for item in result]))
	center('Successfully formatted {}!!'.format(whitelist))
	return result

def gather_followers():
	center('Gathering followers...'.format(whitelist))
	center(' ')
	followers = []
	next_max_id = True
	while next_max_id:
		if next_max_id is True:
			next_max_id = ''
		api.getUserFollowers(api.username_id, maxid=next_max_id)
		api_request = api.LastJson
		old_len = len(followers)
		followers.extend([item['pk'] for item in api_request.get('users', [])])
		next_max_id = api_request.get('next_max_id', '')
		center('Gathered {} followers!!'.format(str(len(followers) - old_len)))
		if next_max_id:
			smart_sleep(delay)
		center(' ')
	if len(followers) == 1:
		center('Successfully gathered {} follower in total!!'.format(len(followers)))
	else:
		center('Successfully gathered {} followers in total!!'.format(len(followers)))
	return followers

def filter_following(following, followers):
	if len(following) == 1:
		print('{}\r'.format(center('Filtering {} currently followed user...'.format(str(len(following))), display=False)), end='')
	else:
		print('{}\r'.format(center('Filtering {} currently followed users...'.format(str(len(following))), display=False)), end='')
	to_unfollow = []
	for item in following:
		if remove_unfollowers and keep_verified:
			if item[0] not in followers:
				if not item[2]:
					to_unfollow.append(item)
		elif remove_unfollowers:
			if item[0] not in followers:
				to_unfollow.append(item)
		elif keep_verified:
			if not item[2]:
				to_unfollow.append(item)
		else:
			to_unfollow.append(item)
	if len(following) == 1:
		center('Successfully filtered {} currently followed user!!'.format(str(len(following))))
	else:
		center('Successfully filtered {} currently followed users!!'.format(str(len(following))))
	center(' ')
	return to_unfollow

def unfollow(to_unfollow):
	count = 0
	if len(to_unfollow) == 1:
		center('{} user to unfollow...'.format(str(len(to_unfollow))))
	else:
		center('{} users to unfollow...'.format(str(len(to_unfollow))))
	center(' ')
	for item in to_unfollow:
		api.unfollow(item[0])
		if not api.LastJson['friendship_status']['following']:
			center('Successfully unfollowed @{}!!'.format(item[1]))
			count += 1
		else:
			center('Unable to unfollow @{}.'.format(item[1]))
		smart_sleep(delay)
		center(' ')
	if count == 1:
		center('Successfully unfollowed {} user!!'.format(str(count)))
	else:
		center('Successfully unfollowed {} users!!'.format(str(count)))

header(False)
blockPrint()
api = InstagramAPI(username, password)
if(api.login()):
	enablePrint()
	center('Signed in as @{}'.format(username))
	center('-', '-')
	api.getSelfUsersFollowing()
	following = [(item['pk'], item['username'], item['is_verified']) for item in api.LastJson['users']]
	if whitelist_all:
		with open(whitelist, 'w') as myfile:
			myfile.write('\n'.join([item[1] for item in following]))
		if len(following) == 1:
			center('Successfully added {} user to {}!!'.format(str(len(following)), whitelist))
		else:
			center('Successfully added {} users to {}!!'.format(str(len(following)), whitelist))
		quit()
	followers = []
	if remove_unfollowers:
		followers = gather_followers()
		header()
	if following:
		to_unfollow = filter_following(following, followers)
	formatted_whitelist = format_whitelist(whitelist)
	header()
	to_unfollow = [item for item in to_unfollow if item[0] not in formatted_whitelist]
	if to_unfollow:
		unfollow(to_unfollow)
	else:
		center('No users to unfollow.')
else:
	enablePrint()
	center('Failed to login.')