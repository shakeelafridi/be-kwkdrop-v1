import datetime
import random
import string

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

try:
    from StringIO import StringIO  ## for Python 2
except ImportError:
    from io import StringIO  ## for Python 3


class Amazon:

    @staticmethod
    def random_string(str_length=16):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(str_length))

    def upload_to_aws(self, name, local_file, ext):
        try:
            current_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            s3_file_name = name + "-" + self.random_string() + "-" + current_time + "." + ext
            s3_file_name = str(s3_file_name)
            data = ContentFile(local_file.read())
            default_storage.save(s3_file_name, data)
            # return True, s3_file_name
            return s3_file_name
        except Exception as e:
            print(e)
            return False, ''

    def upload_to_aws_base64(self, name, local_file, ext):
        try:
            current_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            s3_file_name = name + "-" + self.random_string() + "-" + current_time + "." + ext
            s3_file_name = str(s3_file_name)
            import base64
            image = local_file
            data = ContentFile(base64.b64decode(image), name='temp.jpg')
            # data = ContentFile(local_file.read())
            default_storage.save(s3_file_name, data)
            return s3_file_name
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def upload_to_aws_with_same_name(name, local_file):
        try:
            data = ContentFile(local_file.read())
            default_storage.save(name, data)
            return True, name
        except Exception as e:
            print(e)
            return False, ''

    @staticmethod
    def delete_image_from_aws(name):
        try:
            default_storage.delete(name)
            return True
        except Exception as e:
            print(e)
            return False, ''

    def upload_to_aws_any(self, name, local_file):
        try:
            current_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
            s3_file_name = name + "-" + self.random_string() + "-" + current_time
            s3_file_name = str(s3_file_name)
            data = ContentFile(local_file.read())
            default_storage.save(s3_file_name, data)
            return True, s3_file_name
        except Exception as e:
            print(e)
            return False, ''
