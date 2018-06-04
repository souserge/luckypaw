from django.contrib.auth.models import User
from . import models
from django.core.files import File
import urllib
import os

def associate_user_with_sup(backend, user, response, *args, **kwargs):
    print(response)
    if user is not None:
        sup, created = models.Supervisor.objects.get_or_create(user=user)
        if created:
            name = response.get('name', None)
            if name is not None:
                first_name = name.get('givenName', None)
                last_name = name.get('familyName', None)
                if first_name is not None:
                    user.first_name = first_name
                if last_name is not None:
                    user.last_name = last_name
                user.save()

            sup.user = user
            image = response.get('image', None)
            if image is not None:
                url = image.get('url', None)
                if (url is not None):
                    try:
                        url = url.split('?')[0]
                        local_filename = urllib.request.urlretrieve(url)[0]
                        with open(local_filename, 'rb') as file:
                            sup.photo.save(
                                    os.path.basename(urllib.parse.urlparse(url).path),
                                    File(file)
                                )
                    except:
                        pass

            sup.save()