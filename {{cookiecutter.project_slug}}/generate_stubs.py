from grpc_tools import protoc
import os
gen_path = os.path.abspath(os.path.dirname(__file__))
print(gen_path)
def gen_protos():
    proto_files = []
    
    # gen_path = os.path.abspath(os.getcwd())
    # rootDir = os.path.join(gen_path,'{{cookiecutter.project_slug}}-proto')
    for dirName, subdirList, fileList in os.walk(gen_path):
        for fname in fileList:
            if fname.endswith('.proto'):
                path = os.path.join(dirName, fname)
                proto_files.append(path)

    for path in proto_files:
        print("Generating interface files for :", path)
        protoc.main((
            '',
            f'-I{gen_path}',
            f'--python_out={gen_path}',
            f'--grpc_python_out={gen_path}',
            path,
        ))

if __name__ == "__main__":
    gen_protos()