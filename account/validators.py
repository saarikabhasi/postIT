import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class NumberValidator(object):
    def __init__(self, min_digits=0):
        self.min_digits = min_digits

    def validate(self, password, user=None):
        if not len(re.findall('\d', password)) >= self.min_digits:
            raise ValidationError(
                _("The password must contain at least %(min_digits)d digit(s), 0-9."),
                code='password_no_number',
                params={'min_digits': self.min_digits},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_digits)d digit(s), 0-9." % {'min_digits': self.min_digits}
        )
#validate phone number
def phonenumberValidator(value):
    #phonenumberValidator
    pattern = r'^\+?1?\d{9,15}$'
    if not re.search(pattern,value):
        raise ValidationError(
                _("The phone number must contain  %(min_digits)d digit(s), 9-15."),
                params={'min_digits': 9},
            )
    