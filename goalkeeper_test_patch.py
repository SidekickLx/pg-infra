import logging
import os
import pika
import pickle

from typing import Callable

logger = logging.getLogger(__name__)

parameters = pika.URLParameters(os.environ.get('RABBITMQ_URI', 'amqp://aixcc:ucr_aixcc@aixcc.lyric.today:443/%2F?heartbeat=600'))
connection = pika.BlockingConnection(parameters)

channel = connection.channel()


class RPCClient:
    def __init__(self, func_name) -> None:
        channel = connection.channel()
        self.channel = channel
        self.func_name = func_name

    def __call__(self, *args,func_name=None, **kwds):
        if not func_name:
            func_name = self.func_name
        if not self.channel.is_open:
            global connection
            connection = pika.BlockingConnection(parameters)
            self.channel = connection.channel()
        self.channel.basic_consume('amq.rabbitmq.reply-to', self.on_response, auto_ack=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.func_name,
            properties=pika.BasicProperties(
                reply_to="amq.rabbitmq.reply-to",
            ),
            body=pickle.dumps((args, kwds))
        )
        self.channel.start_consuming()
        return pickle.loads(self.response)

    def progress(self, body):
        p = pickle.loads(body)
        logger.info(f"Received progress: {p}")

    def on_response(self, ch, method, properties, body:bytes):
        logger.debug(f"Received response: {body}")
        if body.startswith(b'SASHI'):
            self.progress(body[5:])
            return
        self.response = body
        self.channel.stop_consuming()


test_patch = RPCClient(f'{os.getenv("CPV_UUID", "linux")}_test_patch')
"""
def test_patch(diff: bytes | str, target: str) -> dict
"""

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'linux':
        if len(sys.argv) > 2:
            print(test_patch(open(sys.argv[2], 'rb').read(), "linux"))
        else:
            print(test_patch("", "linux"))
    else:
        print(f"Usage: python {sys.argv[0]} linux <patch_file>")