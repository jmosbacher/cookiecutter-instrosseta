{% for dependency in cookiecutter.device_dependencies.split(",") %}
import {{dependency}}
{% endfor %}

class {{cookiecutter.DeviceName}}Device():
    def __init__(self, *args, **kwargs):
        ''' Default signature to support directly accepting 
            an rpc message content that may include unused arguments.
        '''

    #FIXME: add communication with physical device here
    # Default access pattern is properties.
    def Connect(self, *args, **kwargs):
        #FIXME: Handle connection to device
        raise NotImplementedError
        return True

    def Disconnect(self, *args, **kwargs):
        raise NotImplementedError
        return True

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
                        **content
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
