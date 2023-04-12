# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META.get('PATH_INFO') == '/graphql':
            token = request.META.get('HTTP_AUTHORIZATION', '')
            
            print('this is the token',token)
            # if not token.startswith('JWT'):
            #     return HttpResponseForbidden('Access Denied')
            jwt_auth = JWTAuthentication()
            auth = None
            try:
                auth = jwt_auth.authenticate(request)
                print(auth)
                if type(auth) is tuple:
                    print(auth[0])
            except Exception:
                return HttpResponseForbidden('Access Denied')
            request.user = auth[0]