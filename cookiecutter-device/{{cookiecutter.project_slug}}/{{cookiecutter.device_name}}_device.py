{%- for dependency in cookiecutter.device_dependencies.split(",") -%}
{% if dependency != '' %}
import {{dependency}}
{% endif %}
{% endfor %}

class {{cookiecutter.DeviceName}}Device():
    def __init__(self, *args, **kwargs):
        pass

    #FIXME: add communication with physical device here
    # Default access pattern is properties.
    {% for name in cookiecutter.method_names.split(",") -%}
    def {{name}}(self, **kwargs):
        raise NotImplementedError

    {% endfor %}

    {% for name in cookiecutter.property_names.split(",") %}
    {%set CamelName = name.split("_")|map("title")|join("") %}
    {%- if name in cookiecutter.option_names -%}
    @property
    def {{name}}_options(self):
        raise NotImplementedError
        return {'options': [],
                'units': 'nan'}
    {% endif %}
    {%- if name in cookiecutter.range_names -%}
    @property
    def {{name}}_range(self):
        return {
            'minimum': float('nan'),
            'maximum': float('nan'),
            'units': 'nan',
        }
    {% endif %}
    {%- if name in cookiecutter.stream_names -%}
    def get_{{name}}_stream(self, **kwargs):
        raise NotImplementedError

    def set_{{name}}(self, **kwargs):
        raise NotImplementedError
    
    {%- elif name in cookiecutter.bstream_names -%}
    def {{CamelName}}(self, request_iterator, context):
        for request in request_iterator:
            #FIXME: Do something with request here.
            resp = pb2.{{CamelName}}Response()
            yield resp

    {%- else -%}
    @property
    def {{name}}(self):
        raise NotImplementedError

    @{{name}}.setter
    def {{name}}(self, value):
        raise NotImplementedError
    {% endif %}
    {% endfor %}
