from instrosetta.interfaces.{{cookiecutter.package_name}} import {{cookiecutter.InterfaceName}}_pb2_grpc as pb2_grpc
from instrosetta.server import RpcServer
from {{cookiecutter.device_name}}_servicer import {{cookiecutter.DeviceName}}Servicer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class {{cookiecutter.DeviceName}}Server(RpcServer):
    @staticmethod
    def bind(sevicer, server):
        pb2_grpc.add_{{cookiecutter.InterfaceName}}Servicer_to_server(sevicer, server)
        
    servicer_class = {{cookiecutter.DeviceName}}Servicer

if __name__ == '__main__':
    {{cookiecutter.DeviceName}}Server().serve('[::]:50052')
