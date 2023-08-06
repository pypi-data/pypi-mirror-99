from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _, get_language_from_request

from .serializers import (
    AuthenticationSerializer,
    UserDetailsSerializer,
    SignupSerializer,
    ForgotPasswordSerializer,
    RecoveryPasswordSerializer,
    LanguageCodeSerializer,
)

# for email notifications
from django.template.loader import get_template

from tg_react.settings import (
    get_password_recovery_url,
    get_post_login_handler,
    get_post_logout_handler,
    get_signup_skipped_fields,
)


def do_login(request, user):
    if hasattr(request, "session"):
        old_session = request.session.session_key

    else:
        old_session = None

    from django.contrib.auth import login  # NOQA

    login(request, user)

    post_login = get_post_login_handler()
    if post_login:
        post_login = import_string(post_login)

        post_login(user=user, request=request, old_session=old_session)


def do_logout(request):
    if hasattr(request, "session"):
        old_session = request.session.session_key

    else:
        old_session = None

    old_user = request.user

    from django.contrib.auth import logout  # NOQA

    logout(request)

    post_logout = get_post_logout_handler()
    if post_logout:
        post_logout = import_string(post_logout)

        post_logout(user=old_user, request=request, old_session=old_session)


class UnsafeSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class UserDetails(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailsSerializer
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return self.request.user

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_authenticated:
            return super().get(request, *args, **kwargs)

        return Response({"authenticated": False}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class AuthenticationView(APIView):
    class UnsafeSessionAuthentication(SessionAuthentication):
        def enforce_csrf(self, request):
            pass

    throttle_classes = ()
    permission_classes = (AllowAny,)
    authentication_classes = (UnsafeSessionAuthentication,)
    serializer_class = AuthenticationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            do_login(request, serializer.user)

            return Response({"success": True})

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class SetLanguageView(generics.RetrieveUpdateAPIView):

    throttle_classes = ()
    permission_classes = (AllowAny,)
    authentication_classes = (UnsafeSessionAuthentication,)
    serializer_class = LanguageCodeSerializer

    @property
    def raw_request(self):
        return self.request._request  # pylint: disable=protected-access

    def get_object(self):
        return {
            "language_code": getattr(
                self.raw_request, "_lang", get_language_from_request(self.raw_request)
            )
        }

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            setattr(
                self.raw_request,
                "update_language_cookie",
                serializer.validated_data["language_code"],
            )
            setattr(
                self.raw_request, "_lang", serializer.validated_data["language_code"]
            )

            return self.get(request, *args, **kwargs)

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        do_logout(request)

        return Response({"success": True})


class SignUpView(APIView):
    serializer_class = SignupSerializer
    permission_classes = (AllowAny,)
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            data = serializer.validated_data.copy()
            password = data.pop("password", None)

            for skipped_field in get_signup_skipped_fields():
                data.pop(skipped_field, None)

            user = get_user_model()(**data)
            user.set_password(password)
            user.save()

            from django.contrib.auth import authenticate  # NOQA

            user = authenticate(email=data["email"], password=password)

            do_login(request, user)

            return Response({"success": True})

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ForgotPassword(APIView):
    """
    Initiate a password restore procedure.
    """

    # Example request data
    # {
    #   "email" : "somename@somedomain.com"
    # }

    serializer_class = ForgotPasswordSerializer
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)

    def send_email_notification(self, user, uid_and_token_b64):
        # define email notification logic
        from django.core.mail import EmailMultiAlternatives  # NOQA

        # make confirm reset url
        path = get_password_recovery_url() % uid_and_token_b64
        confirm_reset_url = settings.SITE_URL + path

        subject = _("Password restore")
        context = {"user": user, "confirm_reset_url": confirm_reset_url}
        text_content = get_template("emails/password_reset.txt").render(context)
        html_content = get_template("emails/password_reset.html").render(context)

        msg = EmailMultiAlternatives(subject, text_content, to=[user.email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.send_email_notification(
                serializer.user, serializer.validated_data["uid_and_token_b64"]
            )
            return Response({"success": True})

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class RestorePassword(APIView):
    """
    Validate token and change a user password.
    """

    # Example request data
    # {
    #   "password" : "asdasd",
    #   "password_confirm" : "asdasd",
    #   "uid_and_token_b64" : "eyJ1aWQiOiAxLCAidG9rZW4iOiAiNDN1LWY5ZDIyMmM4YTNkZDhmYjI2OThlIn0="
    # }

    serializer_class = RecoveryPasswordSerializer
    authentication_classes = (UnsafeSessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"success": True})

        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
