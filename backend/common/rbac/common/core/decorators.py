from functools import wraps

def validation(serializer):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kw):
            data = request.query_params if request.method == 'GET' else request.data
            s = serializer(data=data)
            s.is_valid(raise_exception=True)
            request.params = s.data
            return func(request, *args, **kw)
        return wrapper
    return decorator
