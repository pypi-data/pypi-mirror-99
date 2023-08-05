import simplejson as json

from tracepointdebug.tracepoint.encoder import JSONEncoder
from tracepointdebug.tracepoint.handler import DisableTracePointRequestHandler, \
    EnableTracePointRequestHandler, PutTracePointRequestHandler, RemoveTracePointRequestHandler
from tracepointdebug.tracepoint.handler.update_trace_point_request_handler import UpdateTracePointRequestHandler

REQUEST_HANDLER_MAP = {
    "DisableTracePointRequest": DisableTracePointRequestHandler,
    "EnableTracePointRequest": EnableTracePointRequestHandler,
    "PutTracePointRequest": PutTracePointRequestHandler,
    "RemoveTracePointRequest": RemoveTracePointRequestHandler,
    "UpdateTracePointRequest": UpdateTracePointRequestHandler
}


class BrokerMessageCallback(object):

    def on_message(self, broker_client, message):
        try:
            message = json.loads(message)

            handler = REQUEST_HANDLER_MAP.get(message.get("name"))
            if handler is not None:
                request = handler.get_request_cls()(message)
                response = handler.handle_request(request)
                serialized = json.dumps(response, cls=JSONEncoder)
                broker_client.send(serialized)
            else:
                print("No request handler could be found for message with name {}: {}".format(message.get("name"),
                                                                                              message))
        except Exception as e:
            print(e)
