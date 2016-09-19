# coding=utf-8
import re
from cgi import log

import requests


def getTopic(topicId):
    url = 'https://www.douban.com/group/topic/' + str(topicId)
    return requests.get(url).text

def getGroup(groupId):
    url = 'https://www.douban.com/group/' + str(groupId)
    print url
    return requests.get(url).text

# 获取指定页的所有信息
def getTitleList(groupId = 173252):
    m = {}
    result = []
    NOT_FOUND_KEY = 0
    FOUND_KEY = 1
    STATUS = NOT_FOUND_KEY
    c = getGroup(groupId)
    l = c.split('\n')
    for line in l:
        if STATUS == FOUND_KEY:
            if line.find('<a href="') >= 0 and line.find("topic/") >=0:
                print line
                try:
                    title = line.split('title="')[1].split('" ')[0]
                    url = line.split('href="')[1].split('" ')[0]
                except:
                    log('error:' + line)
                m['title'] = title
                m['url'] = url
                result.append(m)

            if line.find('</table') >=0:
                break

        if line.find(r'<table class="olt">') >= 0:
            STATUS = FOUND_KEY
            continue

    return result

# 获取具体信息
def getTopicContent(topicId = 90823624):
    c = getTopic(topicId)
    NOT_FOUND_KEY = 0
    FOUND_KEY = 1
    STATUS = NOT_FOUND_KEY
    l = c.split('\n')
    content = ''
    for line in l:

        if line.find('<div class="topic-content">') >= 0:
            STATUS = FOUND_KEY

        if STATUS == FOUND_KEY:
            if line.find('<!-- via  -->') >= 0:
                content += "</div>"
                break
            content += line + '\n'
    return content
li = getTopicContent()
print li