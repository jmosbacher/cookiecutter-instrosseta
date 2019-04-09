

if __name__ == "__main__":
    from argparse import ArgumentParser
    from cookiecutter.main import cookiecutter
    from common import read_device_config, read_interface_config
    import os
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="path", default="./interfaces.conf",
                    help="path to device file", metavar="FILE")
    parser.add_argument("-o", "--output", dest="opath", default="./generated_interfaces",
                    help="path to save output", metavar="OFILE")      
    args = parser.parse_args()
    path = args.path
    outdir = args.opath
    interfaces = read_interface_config(path)
    for interface, context in interfaces.items():
        packages = context['package_name'].split('.')
        opath = os.path.join(outdir, *packages)
        cookiecutter('./cookiecutter-interface', no_input=True, overwrite_if_exists=True, extra_context=context, output_dir=opath)

