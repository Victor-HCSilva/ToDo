from django.utils import timezone

def session_timeout_processor(request):
    if not request.user or not request.user.is_authenticated:
        return {'tempo_restante': None}
    
    expiry_date = request.session.get_expiry_date()
    now = timezone.now()
    tempo = expiry_date - now
    return {'tempo_restante': int(tempo.total_seconds()) if tempo.total_seconds() > 0 else 0}