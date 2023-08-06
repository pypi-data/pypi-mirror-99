import json

from ysb_common.constants.constant import Constant


class QueueApi:
    """
    :param header 消息头
    :param body 消息队列中的body
    :param return_data runview中的返回
    """

    @staticmethod
    def retry_check_and_recompose_data(header, body, return_data):
        # 非批量申报任务和外层code不为0的情况（多为登录失败）直接返回
        if header['rwlx'] not in ['4', '20'] or return_data.get('CODE') != '0':
            body['return_data'] = return_data
            return False
        body_return_data = body.get('return_data', None)

        data_node = return_data.get("DATA")
        # key为NSRLXDM value为return_data的DATA中的数据，用于合并结果
        tmp = dict()
        retry_tax = []
        # 检查是否有需要重试的税种，如果有标记NSRLXDM
        for node in data_node:
            tmp[node['NSRLXDM']] = node
            if node['ERROR_CODE'] == '-1':
                retry_tax.append(node.get('NSRLXDM'))

        # 重新组装body中的return_data节点
        if body_return_data is None:
            body['return_data'] = return_data
        else:
            # 替换重复税种的结果
            new_body_return = body['return_data']['DATA'][:]
            for body_return in body['return_data']['DATA']:
                if body_return['NSRLXDM'] in tmp.keys():
                    new_body_return.remove(body_return)
                    new_body_return.append(tmp[body_return['NSRLXDM']])
            body['return_data']['DATA'] = new_body_return

        if len(retry_tax) > 0:  # 有需要重试的税种,重新组装request的参数
            request_data = body.get('DATA')
            tmp = request_data
            for data in request_data:
                if data['NSRLXDM'] not in retry_tax:
                    tmp.remove(data)
            body['DATA'] = tmp
            # header 重试次数加1
            retry_times = header.get('RETRY_TIMES', 0)
            header['RETRY_TIMES'] = retry_times + 1
            if header['RETRY_TIMES'] > 3:
                return False
            return True
        return False
