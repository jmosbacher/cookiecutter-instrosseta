import pint
ureg = pint.UnitRegistry()
Q_ = ureg.Quantity

def accept_text(f):
    def wrapped(*args, **kwargs):
        new_args = [ureg(arg) if isinstance(arg, str) else arg for arg in args]
        new_kwargs = {k:(ureg(kwarg) if isinstance(kwarg, str) else kwarg) for k, kwarg in kwargs.items()}
        return f(*new_args, **new_kwargs)
    return wrapped
