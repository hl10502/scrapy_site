#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

from scrapy_site.common.consts import const

from scrapy_site.utils.log import get_log

sys.path.append('../scrapy_site')
# 获取当前目录，当前目录为scrapy_site项目的根目录
curpath = os.getcwd()
_log = get_log(__name__, curpath + '/scrapy_site/log/email.log')

# 读取文件中内容存储到字符串
def getInfoFromFile(f):
    temp_mail_msg = ''
    # 默认文件中包含文件搜索到的链接信息
    has_Href = None
    while True:
        line = f.readline()
        # 如果读取不为空解析line
        if line:
            print line
            _log.info(line)
            temp = line.split('---')
            if len(temp) == 3:
                if temp[2].strip():
                    temp_mail_msg = temp_mail_msg + "<p>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp" + \
                                    temp[0] + "&nbsp&nbsp" + temp[1] + "<a href='" + temp[
                                        2] + "'>" + "&nbsp&nbsp" + temp[2] + "</a></p>\n"
                    has_Href = True
                else:
                    temp_mail_msg = temp_mail_msg + "<p>" + "&nbsp&nbsp<strong>" + temp[
                        1] + "</strong></p>\n"
                    has_Href = False
            else:
                break
        else:
            break
    # f.close()
    return [temp_mail_msg, has_Href]


# 根据邮箱读取对应网站爬取后的文件
def getMsgByEmail(email):
    mail_msg = ""
    hasHref = []
    spider_names = []

    # 读取email.conf根据对应网站返回邮件内容字符串
    filename = curpath + '/scrapy_site/' + const.EMAIL_CONF
    fc = open(filename, 'r')

    loginfo = "获取文件：" + filename
    # print loginfo
    _log.info(loginfo)

    while True:
        line = fc.readline().strip()
        if line:
            print line
            _log.info(line)
            config = line.split('===')
            receive_emails = config[1]
            if receive_emails == email:
                # 得到邮箱对应的网站
                spider_names = config[0].split(',')
                break
        else:
            break
    fc.close()

    # 读取文件中的内容
    for spider_name in spider_names:
        filename = curpath + '/scrapy_site/msg/' + spider_name
        loginfo = "获取文件：" + filename
        print loginfo
        _log.info(loginfo)

        f = open(filename, 'r')
        temp = getInfoFromFile(f)
        if temp[1]:
            mail_msg = mail_msg + temp[0]
        hasHref.append(temp[1])
        f.close()

    # # 添加上次遗漏信息
    # lastf = open(DIR + '/scrapy_bid/scrapy_bid/lastf.txt', 'r')
    # temp = getInfoFromFile(lastf)
    # if temp[1]:
    #     mail_msg = mail_msg + temp[0]
    # hasHref.append(temp[1])
    # lastf.close()

    isHasHref = True in hasHref
    return [mail_msg, isHasHref]


def sendMail(receiver, creceiver):
    receivers = (receiver + ',' + creceiver).split(',')
    loginfo = "收件人：" + receiver + ",Cc：" +  creceiver
    print loginfo
    _log.info(loginfo)

    temp = getMsgByEmail(receiver)
    mail_msg = temp[0]
    isHasHref = temp[1]
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = const.SENDER
    message['To'] = receiver
    # 如果邮件中含有链接信息则发送给客户
    if isHasHref:
        message.add_header('Cc', creceiver)
    else:
        message.add_header('Cc', const.SENDER)

    # 邮箱主题
    subject = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '招标网站最新信息'
    message['Subject'] = Header(subject, 'utf-8')
    send_result = {}
    send_count = 5
    for send_time in range(0, send_count):
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(const.MAIL_HOST, 25)  # 25 为 SMTP 端口号
            smtpObj.login(const.MAIL_USER, const.MAIL_PASS)
            if isHasHref:
                print '有内容发送给客户'
                _log.info('------有内容发送给客户-----')
                send_result = smtpObj.sendmail(const.SENDER, receivers, message.as_string())
            else:
                print '无内容发送给自己'
                _log.info('------无内容发送给自己-----')
                send_result = smtpObj.sendmail(const.SENDER, const.SENDER, message.as_string())
            print "邮件发送成功"
            _log.info('-----------第{}次发送结果{}----------------'.format(send_time, send_result))
            break
        except smtplib.SMTPException, e:
            _log.error('无法发送邮件:' + str(e))
            print e
            print "Error: 无法发送邮件"


#email.conf配额制文件内容如下：
#b2b10086,bidding,chinaunicombidding===xxx@xx.com,xxx1@xx.com===yyy@yy.com,yyy1@yy.cm
#b2b10086,bidding,chinaunicombidding===xxx@xx2.com,xxx12@xx.com===yyy2@yy.com,yyy12@yy.cm
#以===为间隔本别为需爬网站，邮件接收人，邮件抄送人
#在发送邮件是，sendMail(receiver, creceiver)能够根据receiver邮件接收人读取对应网站文件内容为一个字符串，将该字符串作为邮件内容
#在run.py中读取email.comf读取每行根据收件人生成邮件内容
