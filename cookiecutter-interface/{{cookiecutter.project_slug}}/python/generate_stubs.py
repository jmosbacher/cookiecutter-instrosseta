from grpc_tools import protoc
import os
gen_path = os.path.abspath(os.path.dirname(__file__))
proto_path = os.path.join(*os.path.split(gen_path)[:-1])
def gen_protos():

    path = os.path.join(proto_path,"{{cookiecutter.interface_name}}.proto")
    print("Generating interface files for :", path)
    protoc.main((
        '',
        f'-I{proto_path}',
        f'--python_out={gen_path}',
        f'--grpc_python_out={gen_path}',
        path,
    ))

if __name__ == "__main__":
    gen_protos()