from rest_framework.serializers import ValidationError

from rdmo.core.plugins import get_plugin


class ProviderValidator():

    def __call__(self, data):
        provider_key = data.get('provider_key')
        provider = get_plugin('SERVICE_PROVIDERS', provider_key)
        if provider is None:
            raise ValidationError({
                'provider_key': 'Please provide a valid provider.'
            })

        try:
            options = {option.get('key'): option.get('value') for option in data.get('options', [])}
        except KeyError:
            raise ValidationError({
                'options': 'Options need to be of the form "{"key": "": "value": ""}".'
            })

        for key in options:
            if key not in [field.get('key') for field in provider.fields]:
                raise ValidationError({
                    'options': 'Key "{}" is not valid.'.format(key)
                })

        for field in provider.fields:
            if field.get('required', True) and field.get('key') not in options:
                raise ValidationError({
                    'options': 'Key "{}" is required.'.format(field.get('key'))
                })
