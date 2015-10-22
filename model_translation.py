from django.utils import translation


class TranslatedField(object):
    def __init__(self, en_field, be_field, ru_field):
        self.en_field = en_field
        self.be_field = be_field
        self.ru_field = ru_field

    def __get__(self, instance, owner):
        fields = {
            'en': self.en_field,
            'be': self.be_field,
            'ru': self.ru_field,
        }
        field = fields[translation.get_language()]
        return getattr(instance, field)
