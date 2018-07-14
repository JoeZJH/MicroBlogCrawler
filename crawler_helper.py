# -*- coding:utf8 -*-
import requests
import logging
import time
import json
import os
import re
import markdown
from bs4 import BeautifulSoup

target_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    # 'Connection': 'keep-alive',
    # 'Cookie': 'ajs_user_id=null; ajs_group_id=null; _ga=GA1.2.517667667.1526523301; ajs_anonymous_id=%22513f05e7-2732-4124-aa74-3dfbee43c418%22; _mkto_trk=id:929-FJL-178&token:_mch-docker.com-1526523307626-79689; _gid=GA1.2.215116819.1526888391; mp_82c8a87cfaa9219dff0e89ef744d8357_mixpanel=%7B%22distinct_id%22%3A%20%221636be2346c860-00d080ff043e37-33657f07-13c680-1636be2346d3cd%22%2C%22mp_lib%22%3A%20%22Segment%3A%20web%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
    'DNT': '1',
    'Host': 'store.docker.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}


def get_html(url, params=None, post_data=None):
    """
    get the html by url and params
    :param url: is target url
    :param params: is a dict of params and they have been encoded
    :param post_data: the data(dict) for post, this param will be None when Get method
    :return: a text of html
    """
    if params is not None:
        url += "?"
        for key in params.keys():
            url += "%s=%s&" % (str(key), str(params[key]))
        url = url[0:-1]
    # print "url: [%s]" % url
    # print "proxies: %s" % proxies
    # logging.info("target url: [%s], proxies: [%s]" % (url, proxies))
    # print "get_html: %s" % url
    html = requests.get(url, headers=None)
    # print "url: [%s]\nhtml.text: [%s]" % (url, html.text.encode("utf-8"))
    return html.text


def get_json_data(url, params=None, post_data=None):
    """
    get the json data by url and params(Note: just for the url whose response is a json)
    :param url: is target url
    :param params: is a dict of params has been encoded
    :param post_data: the data(dict) for post, this param will be None when Get method
    :return: a string of json
    """
    json_data = get_html(url, params=params, post_data=post_data)
    # why while statement？
    # because the url have no response sometimes(network or some errors of server)
    # RetryTimes = crawler_config.retry_times
    while json_data is None or json_data == "":
        # RetryTimes -= 1
        # if RetryTimes < 0:
        #     logging.error("Thread: [%s] Retry url: [%s], params: [%s] fail, RetryTimes: [%d]", thread_name, url, params, crawler_config.retry_times)
        #     json_data = None
        #     break
        logging.warning("Retry url: [%s], params: [%s] post_data: [%s]", url, params, post_data)
        print "Warnning: Retry %s" % url
        time.sleep(2)
        json_data = get_html(url, params=params, post_data=post_data)
    # if json_data is None:
    #     thread_name = threading.current_thread
    #     logging.warning("Thread: [%s] Error url: [%s], params: [%s]", thread_name, url, params)
    json_data = json_data.encode("utf-8")
    return json_data


def check_json_format(raw_msg):
    """
    check a msg if could be decoded by json
    :param raw_msg: the raw msg
    :return:
    """
    if isinstance(raw_msg, str):
        try:
            json.loads(raw_msg, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


def find_and_create_dirs(dir_name):
    """
    find dir, create it if it doesn't exist
    :param dir_name: the name of dir
    :return: the name of dir
    """
    if os.path.exists(dir_name) is False:
        os.makedirs(dir_name)
    return dir_name


def write_object_to_file(file_name, target_object):
    """
    write the object to file with json(if the file is exist, this function will overwrite it)
    :param file_name: the name of new file
    :param target_object: the target object for writing
    :return: True if success else False
    """
    dirname = os.path.dirname(file_name)
    find_and_create_dirs(dirname)
    try:
        with open(file_name, "w") as f:
            json.dump(target_object, f, skipkeys=False, ensure_ascii=False, check_circular=True, allow_nan=True, cls=None, indent=True, separators=None, encoding="utf-8", default=None, sort_keys=False)
    except Exception, e:
        message = "Write [%s...] to file [%s] error: json.dump error" % (str(target_object)[0:10], file_name)
        logging.error("%s\n\t%s" % (message, e.message))
        return False
    else:
        # logging.info(get_time() + ": Write " + self.docker_save_path + doc_file_name + ".json")
        logging.info("Write %s" % file_name)
        return True


def read_object_from_file(file_name):
    """
    read a json object from file_name
    :param file_name:
    :return:
    """
    if os.path.exists(file_name) is False:
        logging.error("Error read path: [%s]" % file_name)
        return None
    with open(file_name, 'r') as f:
        try:
            obj = json.load(f)
        except Exception:
            logging.error("Error json: [%s]" % f.read()[0:10])
            return None
    return obj


def remove_links(text):
    """
    remove links for raw_text
    :param text:
    :return: 
    """
    # remove links
    links = re.findall('((http|ftp)s?://.*?(\n| |\0|\v|\t|\r|\f|\000|\b))', text)
    for link in links:
        url = link[0][:-1]
        text = text.replace(url, '')
    # remove emails
    emails = re.findall('((\n| |\0|\v|\t|\r|\f|\000|\b)[0-9a-zA-Z.]+@[0-9a-zA-Z.]+\.[0-9a-zA-Z.]+(\n| |\0|\v|\t|\r|\f|\000|\b))', text)
    for link in emails:
        url = link[0][1:-1]
        text = text.replace(url, '')

    # remove <br />
    brs = re.findall('<br />', text)
    for br in brs:
        text = text.replace(br, '')

    return text


def remove_blank_spaces(text):
    """
    remove black space, including \n, \t and \r
    :param text:
    :return:
    """
    # remove \n
    enters = re.findall('\n', text)
    for enter in enters:
        text = text.replace(enter, '')

    # remove special white space
    text = str(text).strip(u' ​')
    text = str(text).strip()
    return text


def remove_tags(html):
    """
    remove the tags: <code> <a> <img> <table>
    :param html:
    :return:
    """
    html = markdown.markdown(html, ['markdown.extensions.extra'])
    # print html
    soup = BeautifulSoup(html)

    tags = soup.find_all('code')
    for tag in tags:
        # print tag
        tag.decompose()

    tags = soup.find_all('a')
    for tag in tags:
        # print tag
        tag.decompose()

    tags = soup.find_all('img')
    for tag in tags:
        # print tag
        tag.decompose()

    tags = soup.find_all('table')
    for tag in tags:
        # print tag
        tag.decompose()

    text = soup.get_text()
    return text

