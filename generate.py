

if __name__ == "__main__":
    from argparse import ArgumentParser
    from cookiecutter.main import cookiecutter
    import configparser
    import os
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="path", default="./devices.conf",
                    help="path to device file", metavar="FILE")
    parser.add_argument("-o", "--output", dest="opath", default="./generated",
                    help="path to save output", metavar="OFILE")      
    args = parser.parse_args()
    path = args.path
    outdir = args.opath
    
    config = configparser.ConfigParser(delimiters=(':'))
    config.read(path)

    for heading in config.sections():
        interface, manufacturer, device = heading.split(':')
        context = dict(config[heading])
        opath = os.path.join(outdir, interface)
        context.update(interface_name=interface, manufacturer_name=manufacturer, 
                        device_name=device, project_slug=device)
        cookiecutter('./', no_input=True, overwrite_if_exists=True, extra_context=context, output_dir=opath)

