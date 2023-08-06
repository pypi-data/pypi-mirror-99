# wsJsonRpc 
[![License:MIT](https://black.readthedocs.io/en/stable/_static/license.svg)](https://gitlab.com/donalm/wsjsonrpc/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![coverage report](https://gitlab.com/donalm/wsjsonrpc/badges/master/coverage.svg)](https://gitlab.com/donalm/wsjsonrpc/commits/master)
[![pipeline status](https://gitlab.com/donalm/wsjsonrpc/badges/master/pipeline.svg)](https://gitlab.com/donalm/wsjsonrpc/commits/master)
[![python versions](https://img.shields.io/pypi/pyversions/wsjsonrpc)](https://gitlab.com/donalm/wsjsonrpc#tested-versions)

**WsJsonRpc** is a [Twisted Python](https://github.com/twisted/twisted) protocol to support [JSON-RPC 2.0](https://www.jsonrpc.org/specification) over [websocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API). The underlying websocket implementation is provided by [Autobahn](https://github.com/crossbario/autobahn-python).

## Features
Both the client and server endpoints are fully bidirectional. Once the client connects to the server and the server accepts the connection, either endpoint can initiate requests or notifications on the remote side.

## Tested with:
 - Pypy 2.7, 3.6
 - Python 2.7, 3.6, 3.8

## Install
```bash
pip install wsjsonrpc
```

## Usage
A simple server application should expose at least one method to clients. Here we register a `math.sum` method in the API.
```python
#!/usr/bin/env python

import sys

from twisted import logger
from twisted.internet import reactor

from wsjsonrpc import factory

logobserver = logger.textFileLogObserver(sys.stdout)
logger.globalLogPublisher.addObserver(logobserver)

def _sum(protocol, x, y):
    return x + y

if __name__ == "__main__":

    factory = factory.JsonRpcWebSocketServerFactory(u"ws://127.0.0.1:8095/wsjsonrpc")
    factory.registerMethod("math.sum", _sum)

    reactor.listenTCP(8095, factory)
    reactor.run()
```
This client calls that remote `math.sum` method, and then exits.
```python
#!/usr/bin/env python

import sys

from twisted import logger
from twisted.internet import defer
from twisted.internet import task

from wsjsonrpc import factory

logobserver = logger.textFileLogObserver(sys.stdout)
logger.globalLogPublisher.addObserver(logobserver)
log = logger.Logger()

@defer.inlineCallbacks
def main(reactor):

    result = None
    protocol = yield factory.get_client(hostname="localhost", port=8095, path=u"wsjsonrpc")

    """
    Call the 'math.sum' method on our peer and log the result.
    """
    result = yield protocol.request("math.sum", [1, 2])
    log.debug("sum result: {}".format(result))
    yield result

task.react(main)
```
## Batch requests
Both the client and server will accept and process batch requests. Call `request` or `notify` as often as you need to in the batch context. When you exit the context, the batch will be sent to the peer.
```python
#!/usr/bin/env python

import sys

from twisted import logger
from twisted.internet import defer
from twisted.internet import task

from wsjsonrpc import factory

logobserver = logger.textFileLogObserver(sys.stdout)
logger.globalLogPublisher.addObserver(logobserver)
log = logger.Logger()

@defer.inlineCallbacks
def main(reactor):

    protocol = yield factory.get_client(hostname="localhost", port=8095, path=u"wsjsonrpc")

    df = None
    with protocol.batchContext() as batch:
        batch.request("math.sum", [1, 2])
        batch.request("math.sum", [2, 3])
        batch.request("math.sum", [3, 4])
        batch.request("math.sum", [4, 5])
        df = batch.deferredList(consumeErrors=1)

    result = yield df

    log.debug("sum result: {}".format(result))
    yield result

task.react(main)
```
A batch can be submitted without the context manager. The following batch includes two calls to `notify`. Note that the `notify` method does not return a deferred, as notifications do not generate any response from the server.

The `defer.gatherResults` call here does not wait for the `notify` calls to complete - as soon as they are dispatched to the peer they are complete.
```python
    batch = protocol.batch()
    df0 = batch.request("math.sum", [1, 2])
    df1 = batch.request("math.sum", [2, 3])
    batch.notify("math.sum", [3, 4])
    batch.notify("math.sum", [4, 5])

    df = defer.gatherResults(batch.deferreds, consumeErrors=1)
    batch.sendBatch()
    yield df
```
## Implementing an API
Your API methods must take `protocol` as their first argument, and all other arguments should be either positional only or keyword only, for example:
```python
def sum_positional(protocol, x, y):
    return x + y

def sum_keyword(protocol, x=0, y=0):
    return x + y
```
The JSON-RPC spec requires that each request can have one `params` value which MUST be either a `dict`, a `list` or `None`. If WsJsonRpc receives `params` as a list, it expands it into positional arguments:
```python
# client: 
protocol.request("math.sum", [1, 2])
# server:
sum_positional(*params)
```
If it receives `params` as a dict, it expands it into keyword arguments:
```python
# client: 
protocol.request("math.sum", {"x":1, "y":2})
# server:
sum_keyword(**params)
```

## Error handling in your API
If an error occurs in your API, you might want to catch and log that exception, and then raise an exception from the `wsjsonrpc.exception.JsonRpcException` family. The WsJsonRpc protocol will extract the correct error code and message from that exception to return a valid error object to the remote peer.

It's likely that this will be a `JsonRpcInternalError`, but it could also be `JsonRpcMethodNotFound` or a custom subclass of `JsonRpcCustomException` that you have created. See the JSON-RPC documentation of the [Error object](https://www.jsonrpc.org/specification#error_object) for guidance on that.

If your API raises any other exception, WsJsonRpc will repackage that into a `JsonRpcInternalError` which is probably what you want anyway.

## Authentication
Note that on the server side, the first argument that is passed into any API method will be the protocol instance itself. This allows you to write methods that authenticate the client (or peer), and then store the client's identity information as an attribute on your custom protocol implementation.

Subsequent API calls will then be able to access that identity information.

Alternatively, if your WsJsonRpc endpoint is one route in a larger web application, you could use the protocol to access the WebSocket request's authentication cookie.


