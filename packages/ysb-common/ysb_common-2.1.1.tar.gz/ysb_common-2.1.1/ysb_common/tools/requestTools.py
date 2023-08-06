import json
from requests import Session
from bs4 import BeautifulSoup


"""
请求相关类
get_content: 处理请求方法，返回dict类型
"""


class RequestTool:
    # session：共享session；request_type：请求方式，默认get
    @staticmethod
    def get_content(session, url, request_type=None):
        response = session.post(url=url) if request_type else session.get(url=url)
        content_bs = BeautifulSoup(response.text, 'html.parser')
        content_dict = json.loads(content_bs.text)
        return content_dict if isinstance(content_dict, dict) else None

    # 带参数请求
    # add by zlf
    @staticmethod
    def get_qqcontent(session, url, headers=None, request_type=None, qqdata=None):
        response = session.post(url=url, headers=headers, data=json.dumps(qqdata)) if request_type else \
            session.get(url=url)
        content_bs = BeautifulSoup(response.text, 'html.parser')
        content_dict = json.loads(content_bs.text)
        return content_dict if isinstance(content_dict, dict) else None
