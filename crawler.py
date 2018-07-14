# -*- coding:utf8 -*-

import sys
import crawler_helper as ch
import json
import logging
import crawler_config as cc
import os

reload(sys)
sys.setdefaultencoding('utf-8')
cookie = None


def format_user_profile(raw_profile):
    """
    format the raw profile
    :param raw_profile:
    :return: formatted profile
    """
    profile = dict()
    profile["data"] = dict()
    raw_profile = dict(raw_profile)
    if raw_profile.keys().__contains__('ok'):
        profile_flag = raw_profile['ok']
        if profile_flag != cc.RESPONSE_OK_FLAG :
            profile["data"]["statuses"] = list()
        else:
            user = dict()
            raw_user = dict(raw_profile["data"]["user"])
            user["id"] = raw_user["id"]
            user["screen_name"] = raw_user["screen_name"]
            user["statuses_count"] = raw_user["statuses_count"]
            user["gender"] = raw_user["gender"]
            user["followers_count"] = raw_user["followers_count"]
            user["follow_count"] = raw_user["follow_count"]
            profile["data"]["user"] = user

            statuses = list()
            raw_statuses = list(raw_profile["data"]["statuses"])
            for raw_status in raw_statuses:
                raw_status = dict(raw_status)
                if raw_status.keys().__contains__("textLength"):
                    status = dict()
                    status["created_at"] = raw_status["created_at"]
                    status["id"] = raw_status["id"]
                    status["mid"] = raw_status["mid"]
                    status["text"] = raw_status["text"]
                    status["text-length"] = raw_status["textLength"]
                    statuses.append(status)
                else:
                    pass
            profile["data"]["statuses"] = statuses

    return profile


def format_status(raw_status):
    """
    format raw status
    :param raw_status: a dict
    :return: a dict formatted status
    """
    status = dict()
    raw_status = dict(raw_status["data"])
    print raw_status["id"]
    text_length = int(raw_status["textLength"])
    status["text-length"] = text_length
    text = preprocess_text(raw_status["text"])
    status["text"] = text
    return status


def get_status_by_status_id(status_id):
    """
    get status by status id use crawler_config.status_base_url
    :param status_id: the id of status, type is int
    :return: a dict
    """
    params = dict()
    params["id"] = status_id
    status_json = ch.get_json_data(cc.status_base_url, params=params, post_data=None)
    if ch.check_json_format(status_json) is False:
        logging.error("Error to json String: [%s...]", status_json[0:10])
        return None
    raw_status = json.loads(status_json)
    status = format_status(raw_status)
    return status


def get_profile_by_user_id(user_id):
    """
    get profile by user id use crawler_config.profile_base_url
    :param user_id: the id of user, type is int
    :return: a dict
    """
    params = dict()
    params["uid"] = user_id
    profile_json = ch.get_json_data(cc.profile_base_url, params=params, post_data=None)
    if ch.check_json_format(profile_json) is False:
        logging.error("Error profile string to json: [%s...]", profile_json[0:10])
        return None
    raw_profile = json.loads(profile_json)
    profile = format_user_profile(raw_profile)
    # statuses = profile["data"]["statuses"]
    # for status in statuses:
    #     text = status["text"]
    #     print text
    return profile


def get_statuses_by_user_id(user_id):
    """
    get statuses by user id
    :param user_id: the id of user, type is int
    :return: a list of statuses
    """
    profile = get_profile_by_user_id(user_id)
    if profile is None:
        return None
    statuses = list()
    for partial_status in profile["data"]["statuses"]:
        status_id = partial_status["id"]
        status = get_status_by_status_id(status_id)
        if status is None:
            continue
        statuses.append(status)
    return statuses


def preprocess_text(raw_text):
    """
    process text : remove useless chars
    :param raw_text:
    :return:
    """
    text = raw_text
    text = ch.remove_tags(text)
    text = ch.remove_links(text)
    text = ch.remove_blank_spaces(text)
    return text


def crawler_statuses_and_write_to_file():
    """
    crawler statuses and write it to file
    :return:
    """
    user_ids = ch.read_object_from_file(cc.user_ids_path)
    for user_id in user_ids:
        statuses = get_statuses_by_user_id(user_id=user_id)
        if statuses is None:
            logging.warn("statuses is None, user_id: [%s]" % user_id)
        file_name = "statuses_%s.json" % cc.root_user_id
        path = os.path.join(cc.statuses_dir, file_name)
        ch.write_object_to_file(path, statuses)


if __name__ == '__main__':
    crawler_statuses_and_write_to_file()
