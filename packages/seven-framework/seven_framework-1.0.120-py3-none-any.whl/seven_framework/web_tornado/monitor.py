# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-08-05 16:32:25
:LastEditTime: 2021-03-04 14:28:13
:LastEditors: ChenXiaolei
@Description: 监控处理
"""

from seven_framework.config import *
from seven_framework.redis import *
from seven_framework.web_tornado.base_handler.base_api_handler import *


class MonitorHandler(BaseApiHandler):
    def get_async(self):
        """
        @description: 通用监控处理
        @last_editors: ChenXiaolei
        """
        config_monitor = app_config

        # 遍历配置,监控状态
        for key, value in config_monitor.items():
            if type(value) != dict:
                continue

            # Check MYSQL
            if key.find("db") > -1:
                try:
                    MySQLHelper(value).connection()
                except:
                    self.http_response(f"Mysql监控异常:{traceback.format_exc()}")
                    return
            # Check Redis
            elif key.find("redis") > -1:
                now_time = str(time.time)

                try:
                    monitor_key = f"framework_monitor_{config_monitor['run_port']}"

                    redis_client = RedisHelper.redis_init(config_dict=value)

                    redis_client.set(monitor_key, now_time)

                    if redis_client.get(monitor_key).decode() != now_time:
                        self.http_response("Reids监控异常,数据存在存取延迟")
                        return
                except:
                    self.http_response(f"Redis监控异常:{traceback.format_exc()}")
                    return

        self.http_response("ok")
