import grpc
from enum import Enum
import pint
import protobuf_to_dict
from instrosetta.interfaces.{{cookiecutter.package_name}} import {{cookiecutter.interface_name}}_pb2 as pb2
from instrosetta.interfaces.{{cookiecutter.package_name}} import {{cookiecutter.interface_name}}_pb2_grpc as pb2_grpc
from instrosetta.servers.{{cookiecutter.manufacturer_name}}.{{cookiecutter.device_name}}.{{cookiecutter.device_name}}_device import {{cookiecutter.device_name.split("_")|map("title")|join("")}}Device

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


class {{cookiecutter.device_name.split("_")|map("title")|join("")}}Servicer(pb2_grpc.{{cookiecutter.interface_name|title}}Servicer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = {{cookiecutter.device_name.split("_")|map("title")|join("")}}Device()
    {% for name in cookiecutter.property_names.split(",") %}
    {%set CamelName = name.split("_")|map("title")|join("") %}
    def {{CamelName}}(self, request, context):
        try:
            self.device.{{name}}(**request)
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to connect.')
        return pb2.{{CamelName}}Response()
    {% endfor %}
    def Disconnect(self, request, context):
        try:
            self.device.disconnect()
        except:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details('Failed to disconnect.')
        return pb2.DisconnectResponse()


    {% for name in cookiecutter.property_names.split(",") %}
    {%set CamelName = name.split("_")|map("title")|join("") %}
    {%- if name in cookiecutter.option_names -%}
    def Get{{CamelName}}Options(self, request, context):
        resp = pb2.Get{{CamelName}}OptionsResponse()
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            resp = pb2.Get{{CamelName}}OptionsResponse(**self.device.name_options)
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp
    {% endif %}
    {%- if name in cookiecutter.range_names -%}
    def Get{{CamelName}}Range(self, request, context):
        resp = pb2.Get{{CamelName}}RangeResponse()
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            resp = pb2.Get{{CamelName}}RangeResponse(**self.device.name_range)
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp
    {% endif %}
    {%- if name in cookiecutter.stream_names -%}
    def Get{{CamelName}}(self, request, context):
        responses = [] #FIXME: build response iterator here.
        for content in responses:
            resp = pb2.Get{{CamelName}}Response()
            if not self.device.connected:
                context.set_code(grpc.StatusCode.UNAVAILABLE)
                context.set_details('Not connected to any device.')
            else:
                try:
                    resp = pb2.Get{{CamelName}}Response(
                        **self.device.name
                        #FIXME: add response content here.
                    )
                
                except Exception as e:
                    context.set_code(grpc.StatusCode.INTERNAL)
                    context.set_details(f'Device raised exception: {e}')
            yield resp

    def Set{{CamelName}}(self, request_iterator, context):
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        resp = pb2.Set{{CamelName}}Response()
        try:
            self.device.{{name}} = [Q_(request.{{name}}, request.units) for request in request_iterator]
            resp =  pb2.Set{{CamelName}}Response(
                {{name}} = self.device.{{name}},
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp
    
    {%- elif name in cookiecutter.bstream_names -%}
    def {{CamelName}}(self, request_iterator, context):
        for request in request_iterator:
            #FIXME: Do something with request here.
            resp = pb2.{{CamelName}}Response()
            yield resp

    {%- else -%}
    def Get{{CamelName}}(self, request, context):
        resp = pb2.Get{{CamelName}}Response()
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        try:
            resp = pb2.Get{{CamelName}}Response(
                #FIXME: add response content here.
            )
           
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp

    def Set{{CamelName}}(self, request, context):
        if not self.device.connected:
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            context.set_details('Not connected to any device.')
        resp = pb2.Set{{CamelName}}Response()
        try:
            self.device.{{name}} = [Q_(request.{{name}}, request.units)]
            resp =  pb2.Set{{CamelName}}Response(
                {{name}} = self.device.{{name}},
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f'Device raised exception: {e}')
        return resp
    {% endif %}
    {% endfor %}
