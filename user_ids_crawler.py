# -*- coding:utf8 -*-

import sys
import crawler_helper as ch
import json
import logging
import crawler_config as cc
import os
import crawler

save_user_ids = set()
max_size = cc.user_count
new_user_ids = set()


def crawler_user_ids_by_status_id_and_mid(status_id, status_mid):
    """
    get user ids by id and mid of status
    add new user id to save_user_ids and new_user_ids
    :param status_id:
    :param status_mid:
    :return: None
    """
    params = dict()
    params["id"] = status_id
    params["mid"] = status_mid
    params["max_id_type"] = 0
    comments_json = ch.get_json_data(cc.comments_base_url, params=params, post_data=None)
    if ch.check_json_format(comments_json) is False:
        logging.error("Error comments str to json: [%s]", comments_json)
        return False
    raw_comments = json.loads(comments_json)
    raw_comments = dict(raw_comments)
    if raw_comments["ok"] == cc.RESPONSE_OK_FLAG :
        comments_level_1 = raw_comments["data"]["data"]
        if not comments_level_1:
            return
        for comment_level_1 in comments_level_1:
            user_id = comment_level_1["user"]["id"]
            if save_user_ids.__contains__(user_id) is False:
                print user_id
                new_user_ids.add(user_id)
                save_user_ids.add(user_id)
            if save_user_ids.__len__() > max_size :
                return True
            comments = comment_level_1["comments"]
            if not comments:
                continue
            for comment in comments:
                user_id = comment["user"]["id"]
                if save_user_ids.__contains__(user_id) is False:
                    print user_id
                    new_user_ids.add(user_id)
                    save_user_ids.add(user_id)
                if save_user_ids.__len__() > max_size :
                    return True
    return False


def crawler_user_ids_by_root_user_id(curr_user_id):
    """
    get user ids by root user id
    add new user id to save_user_ids and new_user_ids
    this is a recursive function, return until the number of user ids (save_user_ids) more than max_size
    :param curr_user_id:
    :return: None
    """
    profile = crawler.get_profile_by_user_id(curr_user_id)
    if profile is None:
        if new_user_ids.__len__() == 0:
            return
        new_user_id = new_user_ids.pop()
        print "new user id: %d" % new_user_id
        crawler_user_ids_by_root_user_id(new_user_id)
        return

    for partial_status in profile["data"]["statuses"]:
        status_id = partial_status["id"]
        status_mid = partial_status["mid"]
        complete = crawler_user_ids_by_status_id_and_mid(status_id, status_mid)
        if complete:
            return
    if save_user_ids.__len__() < max_size:
        if new_user_ids.__len__() == 0:
            return
        new_user_id = new_user_ids.pop()
        print "new user id: %d" % new_user_id
        crawler_user_ids_by_root_user_id(new_user_id)
        return


def write_save_user_ids_to_file():
    """
    write the result(save_user_ids) to file
    :return:
    """
    old_ids = ch.read_object_from_file(cc.user_ids_path)
    user_ids = set()
    old_ids = set(old_ids)
    if old_ids is not None:
        user_ids = old_ids | save_user_ids
    user_ids = list(user_ids)
    ch.write_object_to_file(cc.user_ids_path, user_ids)


if __name__ == '__main__':
    crawler_user_ids_by_root_user_id(cc.root_user_id)
    write_save_user_ids_to_file()
    print save_user_ids
