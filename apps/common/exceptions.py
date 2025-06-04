from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import NotFound, ValidationError


class ObjectNotFound(NotFound):
    default_detail = _("Not found.")
    default_code = "NOT_FOUND"


class CodeResendError(ValidationError):
    default_detail = "Verification code has already been sent. Wait for a timer to finish."  # noqa
    default_code = "CODE_RESEND_ERROR"


class CodeError(ValidationError):
    default_detail = _("Verification code must be 6 digits.")
    default_code = "VERIFICATION_CODE_ERROR"


class CodeExpiredOrInvalid(ValidationError):
    default_detail = _(" Verification code expired or invalid.")
    default_code = "VERIFICATION_CODE_EXPIRED_OR_INVALID"


class PhoneNumberAlreadyExists(ValidationError):
    default_detail = _("This phone number is linked to another account.")
    default_code = "PHONE_NUMBER_ALREADY_EXISTS"


class PhoneNumberNotFound(NotFound):
    default_detail = _("Phone number is not linked to the account.")
    default_code = "PHONE_NUMBER_NOT_FOUND"


class PhoneNumberNotVerified(ValidationError):
    default_detail = _("Your phone is not verified.")
    default_code = "PHONE_NUMBER_NOT_VERIFIED"
