# encoding: utf-8
from email.mime.application import MIMEApplication

import smtplib
import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .settings import SMTP_HOST, SMTP_USER, SMTP_PWD, SMTP_PORT, SMTP_SENDER, SMTP_TO_LIST

class EmailHelper(object):
    def __init__(self):
        self.smtp_host = SMTP_HOST      # 发送邮件的smtp服务器
        self.smtp_user = SMTP_USER      # 用于登录smtp服务器的用户名，也就是发送者的邮箱
        self.smtp_pwd = SMTP_PWD         # 授权码，和用户名user一起，用于登录smtp， 非邮箱密码
        self.smtp_port = SMTP_PORT          # smtp服务器SSL端口号，默认是465
        self.sender = SMTP_SENDER       # 发送方的邮箱
        self.toLst = SMTP_TO_LIST

    def sendEmailWithAttr(self, send_list):
        dict_result = self.format_data(send_list)
        message = MIMEMultipart()
        # 发件人
        message['From'] = self.sender
        # 收件人列表
        message['To'] = ",".join(self.toLst)
        cur_time_string = datetime.datetime.now().strftime('%Y-%m-%d')


        total_num = 0
        total_titles = ""
        result = "<h1><font color=\"red\">『皮爷撸码』</font>特别提供</h1>"
        for key in dict_result.keys():
            data_list = dict_result[key]
            count_set = set()
            for item in data_list:
                count_set.add(item["video_episode"])
            count_num = len(count_set)
            total_titles = total_titles + "《" + key + "》"
            total_num = total_num = count_num
            result = result + "<h2><font color=\"#006666\">" + key + "</font> 更新了 <font color=\"#ff33cc\">" + str(count_num) + "</font> 集:<h2>\n"
            for item in data_list:
                result = result + self.get_item_result(item)
            result = result + "<h1><font color=\"#ff00ff\">~~~~~~~~~~~~~~~华丽~~的~~分~割~线~~~~~~~~~~~~~~~~~~</font></h1></br>"
        # 邮件标题
        message['Subject'] = cur_time_string + "日，美剧" + total_titles + "总共更新了 " + str(total_num) + " 集"
        print(result)
        message.attach(MIMEText(result, 'html', 'utf-8'))

        try:
            smtpSSLClient = smtplib.SMTP(self.smtp_host, self.smtp_port)   # 实例化一个SMTP_SSL对象
            loginRes = smtpSSLClient.login(self.smtp_user, self.smtp_pwd)      # 登录smtp服务器
            print(f"登录结果：loginRes = {loginRes}")    # loginRes = (235, b'Authentication successful')
            if loginRes and loginRes[0] == 235:
                print(f"登录成功，code = {loginRes[0]}")
                smtpSSLClient.sendmail(self.sender, self.toLst, message.as_string())
                print(f"发送成功. message:{message.as_string()}")
            else:
                print(f"登陆失败，code = {loginRes[0]}")
        except Exception as e:
            print(f"发送失败，Exception: e={e}")

        print("-----------------------发送成功-----------------------")

    def get_item_result(self, item):
        result = "<h3>"
        result = result + "<font color=\"#0033ff\">" + item["video_title_total"] + "</font> ====>>>> 制式：<font color=\"#0033ff\">" + item["video_has_subscribe"] + "</font> ====>>>> 大小：<font color=\"#ff3333\">" + item["video_size"] + "</font></h3>\n"
        if len(item["video_download_magnet"]) != 0:
             result = result + "<h4>迅雷磁力: <a href=\"" + item["video_download_magnet"] + "\"> 下载链接</a></h4>\n"
        if len(item["video_download_ed2k"]) != 0:
            result = result + "<h4>电驴下载: <a href=\"" + item["video_download_ed2k"] + "\"> 下载链接</a></h4>\n"
        if len(item["video_download_bt"]) != 0:
            result = result + "<h4>BT下载: <a href=\"" + item["video_download_bt"] + "\"> 下载链接</a></h4>\n"
        result = result + "</h3>"
        return result

    def format_data(self, send_data):
        result_dict = dict()
        for item in send_data:
            item_name = item["video_title_ch"]
            if item_name in result_dict.keys():
                result_dict[item_name].append(item)
            else:
                temp_list = list()
                temp_list.append(item)
                result_dict[item_name] = temp_list
        for keys in result_dict.keys():
            temp_list = result_dict[keys]
            temp_list.sort(key=lambda k: (k['video_season_episode']), reverse=True)
            temp_list.sort(key=lambda k: (k['video_publish_time'][:-1]), reverse=False)
        return result_dict
