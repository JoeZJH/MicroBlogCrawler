# MicroBlogCrawler
A crawler for Micro-blog with Python Language

* get user ids, the max size of user ids could be set by `user_count`(initial value is 1000 now) in `crawler_config.py`
* get user statuses
* parse the contents of statuses

## files

* user_ids_crawler
	* get user ids and write user ids to file
* crawler
	* read user ids and get statuses(contents) for users

## install
* download this source code
* install necessary modules, including markdown, requests, bs4, json

## run
	# get user ids and write to file
	/usr/bin/python user_ids_crawler.py 
	# get contents of statuses and write to file
	/usr/bin/python crawler.py