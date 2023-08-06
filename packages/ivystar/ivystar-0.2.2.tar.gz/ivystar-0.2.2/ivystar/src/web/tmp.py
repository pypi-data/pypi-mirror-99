import requests_html
!pip install requests_html
!pip install requests_html -i https://pypi.tuna.tsinghua.edu.cn/simple
!pip install requests_html -i https://pypi.tuna.tsinghua.edu.cn/simple
import requests_html
requests_html.HTML
requests_html.get("www.sohu.com")
from requests_html import HTMLSession
session = HTMLSession()
session.get("www.sohu.com")
session.get("http://www.sohu.com")
res = session.get("http://www.sohu.com")
res.html
res.html.html
res.html.html
type(res.html.html)
type(res.html.links)
res.html.links
res.html.absolute_link
res.html.absolute_links
res.html.links
res.html.absolute_links
res.html.html
re.findall("[\u4e00-\u9fa5]", res.html.html)
import re
re.findall("[\u4e00-\u9fa5]", res.html.html)
re.findall("[\u4e00-\u9fa5]*", res.html.html)
re.findall("[\u4e00-\u9fa5]+", res.html.html)
res.html.html
re.findall("[\u4e00-\u9fa5]+", res.html.html)
re.findall("[\u4e00-\u9fa5](?=(水|泥))+", res.html.html)
re.findall("[\u4e00-\u9fa5](?i<=(水|泥))+", res.html.html)
re.findall("[\u4e00-\u9fa5](?<=(水|泥))+", res.html.html)
re.findall("[\u4e00-\u9fa5])+", res.html.html)
re.findall("[\u4e00-\u9fa5]+)", res.html.html)
re.findall("[\u4e00-\u9fa5]+", res.html.html)
set(re.findall("[\u4e00-\u9fa5]+", res.html.html))
len(set(re.findall("[\u4e00-\u9fa5]+", res.html.html)))
len(re.findall("[\u4e00-\u9fa5]+", res.html.html))
len(re.findall("[\u4e00-\u9fa5a-zA-Z\d]+", res.html.html))
re.findall("[\u4e00-\u9fa5a-zA-Z\d]+", res.html.html)
re.findall("[\u4e00-\u9fa5a-zA-Z\d]+", res.html.html)
re.findall("[\u4e00-\u9fa5\d]+", res.html.html)
re.findall("(?=[\u4e00-\u9fa5\d])[^'])", res.html.html)
re.findall("(?=[\u4e00-\u9fa5\d])[^\'])", res.html.html)
re.findall("(?=([\u4e00-\u9fa5\d]))[^\'])", res.html.html)
re.findall("(?=([\u4e00-\u9fa5\d]))[^\'])", res.html.html)
re.findall("(?=([\u4e00-\u9fa5\d])).)", res.html.html)
re.findall("(?=([\u4e00-\u9fa5\d])).*)", res.html.html)
re.findall(".(?=([\u4e00-\u9fa5]))", res.html.html)
re.findall(".(?=([\u4e00-\u9fa5]))+", res.html.html)
re.findall(".+(?=([\u4e00-\u9fa5]))", res.html.html)
re.findall("(.(?=([\u4e00-\u9fa5])))+", res.html.html)
re.findall("(.(?=[\u4e00-\u9fa5]))+", res.html.html)
re.findall(".(?=[\u4e00-\u9fa5])+", res.html.html)
re.findall(".(?=[\u4e00-\u9fa5])*", res.html.html)
re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html)
res.html.html
re.findall("[\u4e00-\u9fa5\da-zA-Z ]+", res.html.html)
re.findall("[\u4e00-\u9fa5\da-zA-Z ！，。、]+", res.html.html)
re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html)
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    print(re.search("[\u4e00-\u9fa5\da-zA-Z]",i))
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    print(re.search("[\u4e00-\u9fa5\da-zA-Z]",i).index)
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    print(re.search("[\u4e00-\u9fa5\da-zA-Z]",i.index))
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    print(re.search("[\u4e00-\u9fa5\da-zA-Z]",i).index)
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    print(re.search("[\u4e00-\u9fa5\da-zA-Z]",i))
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    print(re.search("[\u4e00-\u9fa5]",i))
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    if (re.search("[\u4e00-\u9fa5]",i)):
        print(i)
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    if (re.search("[\u4e00-\u9fa5]",i)):
        print(i)
ii = []
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.html):
    if (re.search("[\u4e00-\u9fa5]",i)):
        print(i)
        ii.append(i)
import collections
collections.Counter(ii)
sorted(collections.Counter(ii))
sorted(collections.Counter(ii).items(), key=lambda x:x[1], reverse=True)
sorted(collections.Counter(ii).items(), key=lambda x:x[1], reverse=True)[:10]
sorted(collections.Counter(ii).items(), key=lambda x:x[1], reverse=True)[:20]
sorted(collections.Counter(ii).items(), key=lambda x:x[1], reverse=True)[:30]
sorted(collections.Counter(ii).items(), key=lambda x:x[1], reverse=True)[:100]
res.html.full_text
res.html.text
res.html.text[0]
res.html.text[1]
res.html.text
ii = []
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.text):
    if (re.search("[\u4e00-\u9fa5]",i)):
        print(i)
        ii.append(i)
ii
for _ in ii:
    if '睡觉' in _:
        print(_)
res.html.text
!grep -a -P '睡觉' res.html.text
cat res.html.text | grep -a -P '睡觉'
!cat res.html.text | grep -a -P '睡觉'
res.html.text | grep -a -P '睡觉'
ii = []
for i in re.findall("[\u4e00-\u9fa5\da-zA-Z]+", res.html.text):
    if '睡觉' in i:
        print(i)
    #if (re.search("[\u4e00-\u9fa5]",i)):
    #    print(i)
    #    ii.append(i)
res.html.full_text
res.html.full_text[0]
res.html.full_text
res.html.full_text.split("\n")
res.html.full_text.split("\\n")
res.html.full_text.split("\n")
res.html.full_text.split(u"\n")
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>0]
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>0]
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>0]
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>0]
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>0]
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>3]
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>3]
res.html.url
res.html.xpath()
res.html.encoding
res.html.time
res.html.page
res.html.page()
res.html.raw_html
[i.strip() for i in res.html.text.split(u"\n") if len(i.strip())>3]
[i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>3]
len([i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>3])
len([i.strip() for i in res.html.text.split(u"\n") if len(i.strip())>3])
b = [i.strip() for i in res.html.text.split(u"\n") if len(i.strip())>3]
a = [i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>3]
b in a
for i in b:
    if i in a:
        pass
    print(i)
ps -af
ls -rlth
ps -af
%hist -f tmp.py
