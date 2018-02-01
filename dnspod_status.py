# -*- coding:utf8 -*-
import requests

LOGIN_EMAIL = 'account'           # 账号
LOGIN_PASSWORD ='password'        # 密码
FORMAT = "json"

DOMAIN_NAME = "sherpper.com"          # 域名
SUB_DOMAIN_NAME = "email"             # 二级域名
VALUE = "abc.diy"                   # 记录的值一定要填写,原来是什么就写什么

RECORD_TYPE = 'A'                   # 记录类型是A或者是CNAME
STATUS = 'enable'                   # 启用 enable，禁用 disable

def domain_info(domain):
    # 登录dnspod，完成其他操作前的基础动作
    url = "https://dnsapi.cn/Domain.Info"
    data = {
        "login_email": LOGIN_EMAIL,
        "login_password": LOGIN_PASSWORD,
        "format": FORMAT,
        "domain": domain
    }
    r = requests.post(url, data=data, timeout=5)
    return r.json()["domain"]

def domain_id(domain):
    # 获取域名ID
    info = domain_info(domain)
    return info["id"]


def record_info(domain, sub_domain):
    # 获取记录相关信息
    url = "https://dnsapi.cn/Record.List"
    data = {
        "login_email": LOGIN_EMAIL,
        "login_password": LOGIN_PASSWORD,
        "format": FORMAT,
        "domain": domain,
        "sub_domain": sub_domain
    }
    r = requests.post(url, data=data, timeout=5)
    return r.json()["records"][0]

def record_data(domain, sub_domain):
    # 获取记录ID，记录的线路，记录的值
    info = record_info(domain, sub_domain)
    return info["id"], info["line"], info["value"]

def record_update(domain, sub_domain):
    # 基于记录的操作
    rid, line, oldip = record_data(domain, sub_domain)
    url = "https://dnsapi.cn/Record.Modify"
    data = {
        "login_email": LOGIN_EMAIL,
        "login_password": LOGIN_PASSWORD,
        "format": FORMAT,
        "domain_id": domain_id(domain),
        "record_id": rid,
        "sub_domain": sub_domain,
        "record_type":RECORD_TYPE,
        "record_line": line,
        "value": VALUE,
        "status": STATUS
    }
    r = requests.post(url, data=data, timeout=5)
    return r.json()

# 修改记录
print record_update(DOMAIN_NAME, SUB_DOMAIN_NAME)


# 获取 record_id, record_line, value
#rid, line, oldip = record_data(DOMAIN_NAME, SUB_DOMAIN_NAME)
#print 'record id:'+ rid
#print 'line: ' + line
#print 'current value: '+ oldip
# 获取 domain_id
#print 'domain id: '+domain_id(DOMAIN_NAME)