# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import random
import json
import crawler_helper
import proxy_config
import os
import logging


def get_proxy_addresses(url, headers):
    """
    crawler proxy addresses web
    :param url: the url of proxy addresses: "http://www.xicidaili.com/nn/"
    :param headers: the headers for getting proxy addresses
    :return: a dict<str(ip:port), protocol> protocol should be https or http
    """
    proxy_html = requests.get(url, headers=headers)
    soup = BeautifulSoup(proxy_html.text, 'lxml')
    rows = soup.find_all('tr')
    # print rows
    proxy_addresses = dict()
    for row in rows:
        tds = row.find_all('td')
        # print tds
        if tds is None or tds.__len__() == 0:
            continue
        protocol = str(tds[5].text).lower()
        ip = tds[1].text
        port = tds[2].text
        proxy_addresses["%s:%s" % (ip, port)] = protocol
    return proxy_addresses


def get_available_proxy_addresses(proxy_url, target_url, proxy_headers):
    """
    get proxy addresses by proxy url and return all available for target url
    :param proxy_url: the url of proxy addresses
    :param target_url: the target url, available proxy addresses are could connect to target url
    :param proxy_headers: the headers for getting proxy addresses
    :return: the available proxy addresses for target url
    """
    proxy_addresses = get_proxy_addresses(proxy_url, proxy_headers)
    if proxy_addresses is None or proxy_addresses.__len__() == 0:
        return None
    available_proxy_addresses = dict()
    for ip in proxy_addresses:
        proxies = {ip: proxy_addresses[ip]}
        try:
            # print "proxies: %s" % proxies
            # print "target_url: %s" % target_url
            html = requests.get(target_url, proxies=proxies)
            # print html.text
        except Exception:
            print "proxies: %s is not available for target url: %s" % (proxies, target_url)
            continue
        if html.status_code == 200:
            available_proxy_addresses[ip] = proxy_addresses[ip]
            print "available proxy: %s://%s" % (proxy_addresses[ip], ip)
    return available_proxy_addresses


def get_random_proxy(proxy_addresses):
    """
    get a random proxy in proxy addresses
    :param proxy_addresses: a dict<str(ip:port), protocol> protocol should be https or http
    :return: a dict <protocol, str(ip:port)> protocol should be https or http
    """
    proxy_ip = random.choice(proxy_addresses.keys())
    proxies = {proxy_ip : proxy_addresses[proxy_ip]}
    return proxies


def get_available_proxy_and_write_to_file(target_url):
    # return
    logging.info("start get proxy...")
    print "start get proxy..."
    proxy_addresses = get_available_proxy_addresses(proxy_config.proxy_url, target_url, proxy_config.proxy_headers)
    crawler_helper.write_object_to_file(proxy_config.proxy_path, proxy_addresses)
    logging.info("write proxy to file [%s]", proxy_config.proxy_path)
    print "done get proxy [%s]" % proxy_config.proxy_path


def get_available_random_proxy():
    proxy_addresses = crawler_helper.read_object_from_file(proxy_config.proxy_path)
    if proxy_addresses is None:
        # return None
        logging.warn("Proxy json file: [%s] doesn't not exists", proxy_config.proxy_path)
        print "Proxy json file: [%s] doesn't not exists" % proxy_config.proxy_path
        return None
    proxy_address = get_random_proxy(proxy_addresses)
    # print proxy_address
    return proxy_address


def test():
    get_available_proxy_and_write_to_file(proxy_config.page_target_url)
    proxy_addresses = crawler_helper.read_object_from_file(proxy_config.proxy_path)
    # print proxy_addresses
    proxy_address = get_random_proxy(proxy_addresses)
    print proxy_address


if __name__ == '__main__':
    test()




    # ip_list = get_proxy_ip_list(url, headers=headers)
    # proxies = get_random_ip(ip_list)
    # print(proxies)
    # # proxy = {"https": "175.11.214.185:808"}
    #
    # for i in range(1, 100):
    #     url = "https://store.docker.com/api/content/v1/products/search?q=%2B&source=community&type=image%2Cbundle&page=1&page_size=" + str(i)
    #     web_data = requests.get(url, proxies=proxies)
    #     jsonData = web_data.text
    #     page = json.loads(jsonData)
    #     if "count" in page:
    #         print "%d count: %d" % (i, page["count"])
    #     else:
    #         break
    # # web_data = requests.get("https://store.docker.com/api/content/v1/products/search?page_size=100&q=%2B&source=community&type=image%2Cbundle&page=1").text
    # # web_data = requests.get("https://store.docker.com/api/content/v1/products/search?q=%2B&source=community&type=image%2Cbundle&page=1849&page_size=100").text
    # # print web_data
