# -*- coding:utf8 -*-
# crawler config file

# https://m.weibo.cn/profile/info?uid=2970452952
profile_base_url = "https://m.weibo.cn/profile/info"
RESPONSE_OK_FLAG = 1

# usage: https://m.weibo.cn/statuses/show?id=4261265310212109
status_base_url = "https://m.weibo.cn/statuses/show"
root_user_id = 2970452952
statuses_dir = "./data/statuses/json/"
user_ids_path = "./data/user-ids/json/user_ids.json"

# usage: https://m.weibo.cn/comments/hotflow?id=4206005635846050&mid=4206005635846050&max_id_type=0
comments_base_url = "https://m.weibo.cn/comments/hotflow"

#
user_count = 1000

