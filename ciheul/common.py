import commands
import sys
import base64
import PIL.Image
import cStringIO
import os.path
import uuid

import settings


class MainResource():
    def alter_list_data_to_serialize(self, request, data_dict):
        data_list = data_dict['objects']
        del(data_dict)
        return data_list


def get_local_ip_address():
    """JUST FOR MAC OS. Linux needs to be implemented."""
    cmd = "ifconfig | grep inet | cut -d ' ' -f2"
    result = commands.getoutput(cmd).split('\n')
    for r in result:
        if '192' in r:
            return r
    return None


def get_ip_port():
    """Get ip address and port for Django settings."""
    if len(sys.argv) == 2:
        ip = '127.0.0.1'
        port = 8000
    elif len(sys.argv) == 3:
        ip = sys.argv[2].split(':')[0]
        if ip == '0.0.0.0':
            ip = get_local_ip_address()
        port = sys.argv[2].split(':')[1]
    return (ip, port)


def b64save_images(b64images):
    for b64image in b64images:
        # decode
        data = base64.b64decode(b64image)

        file_like = cStringIO.StringIO(data)
        img = PIL.Image.open(file_like)

        # TODO investigate whether uuid is indeed unique
        # generate random filename
        image_name = generate_random_filename() + '.jpg'

        img.save(os.path.join(settings.PROJECT_PATH, 'static/img', image_name))


def generate_random_filename():
    return str(uuid.uuid4())
