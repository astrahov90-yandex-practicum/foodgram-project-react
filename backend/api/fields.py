import base64
import uuid
import os

from django.core.files.base import ContentFile
from django.conf import settings
from rest_framework import serializers

import six


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through
    raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = '%s.%s' % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = 'jpg' if extension == 'jpeg' else extension

        return extension

    def to_representation(self, value):

        format = 'png'
        image_file = settings.MEDIA_ROOT + value.path

        if not os.path.isfile(image_file):
            return None

        encoded_string = ''
        with open(image_file, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read())
        return 'data:image/%s;base64,%s' % (format, encoded_string)
