from django.core.exceptions import ValidationError
from django.conf import settings
from main import models

from random import randint
from slugify import slugify
from datetime import datetime

import os
import requests
import random
import string


def random_string_generator(
    size=10, chars=string.ascii_lowercase + string.digits
) -> str:
    return "".join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None) -> str:

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    _Class = instance.__class__
    qs_exists = _Class.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def check_inn(inn) -> bool:

    if len(inn) not in (10, 12):
        return False

    def inn_csum(inn):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11 - len(inn) :], [int(x) for x in inn])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    if len(inn) == 10:
        return inn[-1] == inn_csum(inn[:-1])
    else:
        return inn[-2:] == inn_csum(inn[:-2]) + inn_csum(inn[:-1])


def validate_inn(inn):

    print(check_inn(inn))
    if not check_inn(inn):
        print("Not inn")
        raise ValidationError(
            "Tax %(value)s - is incorrect! Please enter a valid Tax code",
            params={"value": inn},
        )


def inn_ctrl_summ(nums, type):
    """
    calculating inn control sum
    """
    inn_ctrl_type = {
        "n2_12": [7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        "n1_12": [3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8],
        "n1_10": [2, 4, 10, 3, 5, 9, 4, 6, 8],
    }
    n = 0
    l = inn_ctrl_type[type]
    for i in range(0, len(l)):
        n += nums[i] * l[i]
    return n % 11 % 10


def inn_gen(length=None):
    """
    INN generation (10 12 digits)
    input accepts - 10 or 12.
    if no length give random length will be selected.
    """
    if not length:
        length = list((10, 12))[randint(0, 1)]
    if length not in (10, 12):
        return None
    nums = [
        randint(1, 9) if x == 0 else randint(0, 9)
        for x in range(0, 9 if length == 10 else 10)
    ]
    if length == 12:
        n2 = inn_ctrl_summ(nums, "n2_12")
        nums.append(n2)
        n1 = inn_ctrl_summ(nums, "n1_12")
        nums.append(n1)
    elif length == 10:
        n1 = inn_ctrl_summ(nums, "n1_10")
        nums.append(n1)
    return "".join([str(x) for x in nums])


def download_image_from_url(pic_url):
    upload_dir = os.path.join(os.path.join(settings.MEDIA_ROOT, "uploads"), "cars")
    now_filename = datetime.now().strftime("%Y%m%d%H%M%S%f") + ".jpg"
    image_filename = os.path.join(upload_dir, now_filename)
    with open(image_filename, "wb") as handle:
        response = requests.get(pic_url, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return now_filename


def generate_phone():

    """
    generates a unique phone number to avoid UNIQUE constraint error in tests
    """

    number = "+44" + str(random.randint(10000000000, 99999999999))
    objects_pool = models.Seller.objects.filter(phone_number=number)
    while objects_pool.exists():
        number = "+44" + str(random.randint(10000000000, 99999999999))
        objects_pool = models.Seller.objects.filter(phone_number=number)
    return number
