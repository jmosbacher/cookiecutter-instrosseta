import configparser

def read_interface_config(path):
    config = configparser.ConfigParser(delimiters=(':'))
    config.read(path)
    interfaces = {}

    for heading in config.sections():
        package, interface = heading.split(':')
        context = dict(config[heading])
        context.update(interface_name=interface, package_name=package, 
                    project_slug=interface)
        interfaces[interface] = context
    return interfaces
    
def read_device_config(path):
    config = configparser.ConfigParser(delimiters=(':'))
    config.read(path)
    devices = {}
    for heading in config.sections():
        interface, manufacturer, device = heading.split(':')
        context = dict(config[heading])
        context.update(interface_name=interface, manufacturer_name=manufacturer, 
                        device_name=device, project_slug=device)
        devices[(interface, manufacturer, device)] = context
    return devices