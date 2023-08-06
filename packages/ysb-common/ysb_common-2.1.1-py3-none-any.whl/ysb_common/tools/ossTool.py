# -*- coding: utf-8 -*-
import os
import time
import traceback

import oss2

from ysb_common.constants.constant import Constant


class OssToolCls:
    """
    截图上传工具类
    """

    @staticmethod
    def put_file(key, secret, bucket, path, local_path):
        """
        上传本地文件到oss存储
        :param key:
        :param secret:
        :param bucket:
        :param path:
        :param local_path:
        :return: 响应码 ”200“ 上传成功
        """
        auth = oss2.Auth(key, secret)
        bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', bucket)

        # <path>上传文件到OSS时需要指定包含文件后缀在内的完整路径，例如abc/efg/123.jpg。
        # <local_path>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt。
        result = bucket.put_object_from_file(path, local_path)
        return str(result.status)

    @staticmethod
    def sb_error_screenshot(return_data, driver, nsrsbh, path_prefix, key, secret, bucket_name):
        """
                上传申报异常截图
                :param driver:
                :param nsrsbh:税号
                :param path_prefix:前置路径
                :return: 响应码 ”200“ 上传成功
        """
        if return_data['CODE'] == "-1" and "已申报" not in return_data['MSG'] and "已报送" not in return_data['MSG']:
            try:
                times = time.strftime("%Y%m", time.localtime())
                nsrlx_dm = return_data['NSRLXDM']
                file_name = nsrlx_dm + '_' + str(int(round(time.time() * 1000))) + '.png'
                local_file = path_prefix + file_name
                remote_path = "sbycjt/" + str(times) + "/" + nsrsbh + "/" + file_name

                driver.get_screenshot_as_file(local_file)

                auth = oss2.Auth(key, secret)
                bucket = oss2.Bucket(auth, 'http://oss-cn-beijing.aliyuncs.com', bucket_name)
                result = bucket.put_object_from_file(remote_path, local_file)

                if str(result.status) == "200":
                    os.remove(local_file)
                    return_data['ERROR_IMG'] = remote_path
            except Exception as e:
                print(e)
                print(traceback.format_exc())