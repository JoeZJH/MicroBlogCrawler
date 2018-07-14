# -*- coding:utf8 -*-




import sys
import os
import crawler_config as cc
import crawler_helper as ch

reload(sys)
sys.setdefaultencoding("utf-8")

def parse_contents_from_files():
    base_path = cc.statuses_dir
    filenames = os.listdir(base_path)
    contents = list()
    for filename in filenames:
        raw_json_path = os.path.join(base_path, filename)
        statuses = ch.read_object_from_file(raw_json_path)
        if statuses is None:
            print filename, "is None"
            continue
        for status in statuses:
            contents.append(status["text"])
    return contents


def write_contents_to_file(contents):
    ch.find_and_create_dirs(os.path.dirname(cc.contents_path))
    print os.path.dirname(cc.contents_path)
    with open(cc.contents_path, 'w') as fp:
        for content in contents:
            fp.write(content)
            fp.write("\n")


if __name__ == '__main__':
    all_contents = parse_contents_from_files()
    write_contents_to_file(all_contents)



