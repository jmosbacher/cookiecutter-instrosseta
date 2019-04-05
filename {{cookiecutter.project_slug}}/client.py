import grpc

class RpcClient:
    stub_class = lambda channel : None

    def __init__(self, stub_class, addr="localhost:50052"):
        self.addr = addr 
        self._channel = None
        self._stub = None
       
    def _single_rpc(self, method, request):
        try:
            resp = getattr(self._stub, method)(request)
            return resp
        except grpc.RpcError as e:
            print(e)
            # FIXME: log error/ raise exception.

    def single_rpc(self, method, request):
        if self._channel is None:
            with self as s:
                return s._single_rpc(method, request)
        else:
            return self._single_rpc(method, request)

    def _streaming_rpc(self, method, request):
        try:
            for resp in getattr(self._stub, method)(request):
                yield resp
        except grpc.RpcError as e:
            print(e)
            # FIXME: log error/ raise exception.
            #    
    def streaming_rpc(self, method, request):
        if self._channel is None:
            with self as s:
                for resp in s._streaming_rpc(method, request):
                    yield resp
        else:
            for resp in self._streaming_rpc(method, request):
                    yield resp
            
    def bstream_rpc(self, request_generator):
        raise NotImplementedError

    def send_stream_rpc(self, request_generator):
        raise NotImplementedError
    
    def __enter__(self):
        self._channel = grpc.insecure_channel(self.addr)
        self._stub = self.stub_class(self._channel)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._channel.close()
        self._channel = None
        self._stub = None