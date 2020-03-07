from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from mtm.settings import PASSWORD_REGEX

def validate_password(value):
    if not PASSWORD_REGEX.match(value):
        raise ValidationError(
            _('Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one number, and one special character: !@#$%^&*()?'),
            code='invalid'
        )
