from instrosetta.interfaces.{{cookiecutter.package_name}} import {{cookiecutter.interface_name}}_pb2_grpc as pb2_grpc
from instrosetta.server import RpcServer
from {{cookiecutter.device_name}}_servicer import {{cookiecutter.device_name|title}}Servicer

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class {{cookiecutter.device_name|title}}Server(RpcServer):
    @staticmethod
    def bind(sevicer, server):
        pb2_grpc.add_{{cookiecutter.interface_name|title}}Servicer_to_server(sevicer, server)
        
    servicer_class = {{cookiecutter.device_name|title}}Servicer

if __name__ == '__main__':
    {{cookiecutter.device_name|title}}Server().serve('[::]:50052')
