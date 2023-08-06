# Neo Python SDK

## Installation

`pip install neo-python-sdk`

## Usage

To use it you have to import it in Python with following import:

`import neo-python-sdk as Neo`

### Example

```Python
# processing tasks requires a queue name
# the request object will be passed to the provided processor (a function)
# the "processor" should use async / await
async def start_neo_tasks(loop):
    neo = Neo.NeoNatsClient()
    await neo.connect(loop=loop)
    async def process_request(payload):
      res = f'Hi there, {payload['user']}'
      return res

    await neo.process("nsx.dev.example.sayHello", process_request)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_neo_tasks(loop))
    loop.run_forever()


# the task / message can contain anything
# for best compatibility it should be a particle
neo = Neo.NeoNatsClient()
await neo.connect(loop=loop)
neo.create('nsx.dev.example.sayHello', {
  user: 'John',
})

```