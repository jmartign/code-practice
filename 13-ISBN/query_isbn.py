# coding:utf-8

# https://developers.douban.com/wiki/?title=book_v2#get_isbn_book
# https://github.com/douban/douban-client

from contextlib import closing
import codecs
import requests


def query_douban(isbn):
    url = 'https://api.douban.com/v2/book/isbn/%s' % isbn
    r = requests.get(url)
    return r.json()['title']


def gen_isbn_barcode(isbn):
    url = 'http://b.wwei.cn/html/image.php'
    payload = {
        'filetype':'PNG',
        'dpi': 72,
        'scale': 2,
        'rotation': 0,
        'font_family': 'Arial.ttf',
        'font_size': 12,
        'text': isbn,
        'thickness': 30,
        'code': 'BCGisbn',
    }
    filename = '%s.png' % isbn
    with closing(requests.get(url, params=payload)) as r:
        fd = open(filename, 'wb')
        for chunk in r.iter_content(4096):
            fd.write(chunk)
        fd.flush()
        fd.close()
    return filename


def main():
    outfd  = codecs.open('out.txt', 'w', 'utf-8')
    for line in open('q.txt'):
        line = line.strip()
        if line:
            title = query_douban(line)
            outfd.write(u'%s %s\n' % (line, title))
            gen_isbn_barcode(line)
    outfd.close()

if __name__ == '__main__':
    main()
