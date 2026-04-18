from .models import User


def accounts_user(request):
    uid = request.session.get('user_id')
    if not uid:
        return {'accounts_user': None}
    try:
        return {'accounts_user': User.objects.get(pk=uid)}
    except User.DoesNotExist:
        return {'accounts_user': None}
