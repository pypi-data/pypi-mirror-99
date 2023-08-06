from nats.aio.client import Client as NATS
import json
import os
import logging
from sentry_sdk import capture_exception


class NeoNatsClient(NATS):
    def __init__(self):
        log_format = "%(asctime)-15s[NSX][%(levelname)s] %(message)s"

        logging.basicConfig(format=log_format, level=logging.DEBUG)
        self.logger = logging.getLogger("nsx")

        self.npq_host = os.getenv("NPQ_HOST", "127.0.0.1")
        self.npq_pass = os.getenv("NPQ_PASS", "local")
        self.npq_port = os.getenv("NPQ_PORT", "4222")
        self.npq_user = os.getenv("NPQ_USER", "neo")
        self.sentry_dsn = os.getenv("SENTRY_DSN")

    async def connect(self, loop):
        await super().connect(
            f"nats://{self.npq_host}:{self.npq_port}",
            user=self.npq_user,
            password=self.npq_pass,
            io_loop=loop,
        )
        self.logger.info(f"Connected to nats://{self.npq_host}:{self.npq_port}")

    async def process(self, queue, processor):
        async def process_handler(msg):
            subject = msg.subject
            reply = msg.reply
            payload = json.loads(msg.data.decode())
            self.logger.info(f"Received a message on '{subject}'")
            try:
                result = await processor(payload)
            except Exception as e:
                capture_exception(e)
            await self.publish(reply, json.dumps(result).encode())

        await super().subscribe(queue, cb=process_handler)
        self.logger.info(f"Subscribed to {queue}")

    async def create(self, queue, particle={}, options={"timeout": 15000}):
        try:
            result = await super().request(
                queue, json.dumps(particle).encode(), timeout=options["timeout"]
            )
        except Exception as e:
            capture_exception(e)
        return json.loads(result.data.decode())

    async def capture_exception(self, e):
        capture_exception(e)
