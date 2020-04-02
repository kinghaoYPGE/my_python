# coding:utf-8

import hashlib
from flask import Flask, request, make_response
import xml.etree.ElementTree as tree
import requests
from lxml import etree
from random import choice

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        print('coming Get')
        data = request.args
        token = 'kinghao'  # 在此处使用
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')
        s = [timestamp, nonce, token]
        s.sort()
        s = ''.join(s)
        print(s)
        if hashlib.sha1(s.encode('utf8')).hexdigest() == signature:
            print('auth successfully')
            return make_response(echostr)

    if request.method == 'POST':
        xml_str = request.stream.read()
        xml = tree.fromstring(xml_str)
        to_username = xml.find('ToUserName').text
        from_username = xml.find('FromUserName').text
        create_time = xml.find('CreateTime').text
        msg_type = xml.find('MsgType').text
        content = xml.find('Content').text
        msg_id = xml.find('MsgId').text

        reply_xml = '''
        <xml>
        <ToUserName><![CDATA[{0}]]></ToUserName>
        <FromUserName><![CDATA[{1}]]></FromUserName>
        <CreateTime>{2}</CreateTime>
        <MsgType><![CDATA[{3}]]></MsgType>
        <Content><![CDATA[{4}]]></Content>
        </xml>
        '''

        if msg_type == 'text':
            # if type(content).__name__ == 'unicode':
            #     content = content.encode('utf-8')
            if '笑话' in content:
                content = fetch_jokes('https://www.qiushibaike.com/text/')
            else:
                content = content[::-1]
        else:
            content = '我们目前只能支持文字，敬请期待！'
        reply = reply_xml.format(from_username, to_username, create_time, msg_type, content)
        print(reply)
        return reply


def fetch_jokes(url):
    r = requests.get(url)
    html = etree.HTML(r.text)
    joke_list = html.xpath('//*[@id="content-left"]//div[@class="content"]//span[1]//text()')

    return choice([joke.strip('\n') for joke in joke_list])


if __name__ == "__main__":
    app.run(port=8089, debug=True)
