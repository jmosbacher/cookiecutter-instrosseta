import grpc
from enum import Enum
import pint
import protobuf_to_dict
from .utils.units import accept_text
import {{cookiecutter.package_name}}.{{cookiecutter.interface_name}}_pb2 as pb2
import {{cookiecutter.package_name}}.{{cookiecutter.interface_name}}_pb2_grpc as pb2_grpc
from instrosetta.client import RpcClient

ureg = pint.UnitRegistry()
Q_ = ureg.Quantity


class {{cookiecutter.InterfaceName}}(RpcClient):
    {% for name in cookiecutter.method_names.split(",") -%}
    {%- set CamelName = name.split("_")|map("title")|join("") -%}
    def {{name}}(self, **kwargs):
        req = pb2.{{CamelName}}Request(**kwargs)
        resp = self.single_rpc("{{CamelName}}", req)
        if resp is not None:
            return protobuf_to_dict(resp)

    {% endfor %}
    {% for name in cookiecutter.property_names.split(",") -%}
    {%- set CamelName = name.split("_")|map("title")|join("") -%}
    {%- if name in cookiecutter.stream_names -%}
    def {{name}}_stream(self):
        req = pb2.Get{{CamelName}}Request()
        for resp in self.stream_rpc("Get{{CamelName}}", req):
            if resp is not None:
                yield Q_(resp.value, resp.units)
            else:
                yield Q_(float('nan'))

    {%- elif name in cookiecutter.bstream_names -%}
    def {{name}}(self):
        def request_generator():
            yield pb2.{{CamelName}}Request()

        response_iterator = self.double_stream_rpc("{{CamelName}}", request_generator())
        for resp in response_iterator:
            if resp is not None:
                yield Q_(resp.value, resp.units)
            else:
                yield Q_(float('nan'))

    {%- else -%}
    @property
    def {{name}}(self):
        req = pb2.Get{{CamelName}}Request()
        resp = self.single_rpc("Get{{CamelName}}", req)
        if resp is not None:
            return Q_(resp.value, resp.units)
        else:
            return Q_(float('nan'))

    {% endif%}
    {%- if name in cookiecutter.option_names -%}
    @{{name}}.setter       
    @accept_text
    def {{name}}(self, value):
        resp = self.single_rpc("Get{{CamelName}}Options", req)
        if value in resp.options:
            req = pb2.Set{{CamelName}}Request(value=value.magnitude, units=str(value.unit))
            self.single_rpc("Set{{CamelName}}", req)
        else:
            raise ValueError(f"{{name}} must be one of {resp.options}")

    {%- elif name in cookiecutter.range_names -%}
    @{{name}}.setter       
    @accept_text
    def {{name}}(self, value):
        resp = self.single_rpc("Get{{CamelName}}Range", req)
        if  resp.minimum <= value <= resp.maximum:
            req = pb2.Set{{CamelName}}Request(value=value.magnitude, units=str(value.unit))
            self.single_rpc("Set{{CamelName}}", req)
        else:
            raise ValueError(f"{{name}} must be between {resp.minimum} and {resp.maximum}")

    {%- elif name in cookiecutter.stream_names -%}
    {%- elif name in cookiecutter.bstream_names -%}
    {%- else -%}
    @{{name}}.setter       
    @accept_text
    def {{name}}(self, value):
        req = pb2.Set{{CamelName}}Request()
        self.single_rpc("Set{{CamelName}}", req)

    {% endif %}
    {% endfor %}


