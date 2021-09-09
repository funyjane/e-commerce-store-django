from django.core.exceptions import ValidationError
from slugify import slugify
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
        slug = slugify(instance.name)

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
