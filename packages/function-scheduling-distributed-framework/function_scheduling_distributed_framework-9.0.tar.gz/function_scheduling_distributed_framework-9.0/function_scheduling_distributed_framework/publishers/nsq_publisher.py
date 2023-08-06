# -*- coding: utf-8 -*-
# @Author  : ydf
# @Time    : 2019/8/19 0008 12:12

from gnsq import Producer, NsqdHTTPClient
from gnsq.errors import NSQHttpError
from function_scheduling_distributed_framework.publishers.base_publisher import AbstractPublisher
from function_scheduling_distributed_framework import frame_config


class NsqPublisher(AbstractPublisher, ):
    """
    使用nsq作为中间件
    """

    # noinspection PyAttributeOutsideInit
    def custom_init(self):
        self._nsqd_cleint = NsqdHTTPClient(frame_config.NSQD_HTTP_CLIENT_HOST, frame_config.NSQD_HTTP_CLIENT_PORT)
        self._producer = Producer(frame_config.NSQD_TCP_ADDRESSES)
        self._producer.start()

    def concrete_realization_of_publish(self, msg):
        # noinspection PyTypeChecker
        self._producer.publish(self._queue_name, msg.encode())

    def clear(self):
        try:
            self._nsqd_cleint.empty_topic(self._queue_name)
        except NSQHttpError as e:
            self.logger.exception(e)  # 不能清除一个不存在的topoc会报错，和其他消息队列中间件不同。
        self.logger.warning(f'清除 {self._queue_name} topic中的消息成功')

    def get_message_count(self):
        return self._nsqd_cleint.stats(self._queue_name)['topics'][0]['message_count']

    def close(self):
        self._producer.close()




