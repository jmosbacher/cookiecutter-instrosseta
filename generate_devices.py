

if __name__ == "__main__":
    from argparse import ArgumentParser
    from cookiecutter.main import cookiecutter
    from common import read_device_config, read_interface_config
    import os
    parser = ArgumentParser()
    parser.add_argument("-df", "--dfile", dest="dpath", default="./devices.conf",
                    help="path to device file", metavar="FILE")
    parser.add_argument("-if", "--ifile", dest="ipath", default="./interfaces.conf",
                    help="path to device file", metavar="FILE")
    parser.add_argument("-o", "--output", dest="opath", default="./generated_devices",
                    help="path to save output", metavar="OFILE")      
    args = parser.parse_args()
    outdir = args.opath
    
    devices = read_device_config(args.dpath)
    interfaces = read_interface_config(args.ipath)
    for (interface, manufacturer, device), context in devices.items():
        opath = os.path.join(outdir, manufacturer)
        context.update(**interfaces[interface])
        cookiecutter('./cookiecutter-device', no_input=True, overwrite_if_exists=True, extra_context=context, output_dir=opath)
