import threading

_thread_locals = threading.local()


def get_current_user():
    """Retorna o usuário da requisição atual de forma global."""
    return getattr(_thread_locals, "user", None)


class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Guarda o usuário no thread local antes de processar a requisição
        _thread_locals.user = getattr(request, "user", None)
        response = self.get_response(request)

        # Limpa após finalizar a requisição por segurança
        if hasattr(_thread_locals, "user"):
            del _thread_locals.user

        return response
