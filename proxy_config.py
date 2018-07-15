# -*- coding: utf-8 -*-

proxy_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
proxy_url = "http://www.xicidaili.com/nn/"
page_target_url = "https://m.weibo.cn/comments/hotflow?id=4206005635846050&mid=4206005635846050&max_id_type=0"

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

proxy_path = "./data/proxy/json/proxy.json"
# print proxy_path