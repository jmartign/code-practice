# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
import opencc
import base62

rawurl = "http://weibo.com/2803301701/CeaOU15IT"
cc = opencc.OpenCC("t2s")

p = re.compile(r"weibo\.com/(\d+)/(\w+)")
m = re.findall(p,rawurl)
if m:
    uid = m[0][0]
    mid = m[0][1]
    id = base62.mid2id(mid)
url = "http://tw.weibo.com/{0}/{1}".format(uid,id)
print u"微博台湾站链接:{0}".format(url)

user_agent = {'User-agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
r = requests.get(url,headers=user_agent)
soup = BeautifulSoup(r.text)
name = soup.find("div","name")
t_name = name.h1.a.text
s_name = cc.convert(name.h1.a.text)
link = name.h1.a["href"]
weibotext = soup.find("p",id="original_text")
t_weibotext = weibotext.text.strip()
s_weibotext = cc.convert(weibotext.text.strip())

print u"繁体中文版-->\n用户:{0}\t用户主页:{1}\n微博内容:{2}".format(t_name,link,t_weibotext)
print u"简体中文版-->\n用户:{0}\t用户主页:{1}\n微博内容:{2}".format(s_name,link,s_weibotext)
