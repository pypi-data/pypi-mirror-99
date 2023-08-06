from django.core.management.base import BaseCommand
from django_reaktion_crm.models import Clients
from django.db.utils import IntegrityError
import csv
import base64

"""
Mapping for import/HJA
"""
EMAIL = 0
FIRST_NAME = 1
LAST_NAME = 2
WORK_POSITION = 3
PHONE = 4
COMPANY = 5
ORG_NUMBER = 6
UID = 7


class Command(BaseCommand):
    help = 'Import csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs='+', type=str)

    def handle(self, *args, **options):

        filename = ''
        if options['filename']:
            filename = f"{options['filename'][1]}"
        else:
            print("Filename is missing")
            exit(0)

        with open(filename, 'r') as cv:
            data = csv.reader(cv, delimiter=',')
            wrong_pad = []
            value_error = []
            for item in data:
                if item[UID]:
                    print(item[UID])
                    try:
                        if "=" in item[UID]:
                            uid_v = item[UID]
                        else:
                            uid_v = f"{item[UID]}="

                        uid = base64.b64decode(uid_v)

                        obj, created = Clients.objects.get_or_create(
                            email=item[EMAIL],
                            defaults={
                                'name': f"{item[FIRST_NAME]} {item[LAST_NAME]}",
                                'phone': item[PHONE],
                                'org_number': item[ORG_NUMBER],
                                'company': item[COMPANY],
                                'position': item[WORK_POSITION],
                                'uid': uid,
                            }
                        )
                    except base64.binascii.Error:
                        wrong_pad.append(uid)
                        print(f"Padding is wrong -> {uid}")
                        continue
                    except IntegrityError:
                        print(f"Duplicated uid -> {uid}")
                        continue
                    except ValueError:
                        value_error.append(uid)
                        continue

        print(list(set(wrong_pad)))
        print(list(set(value_error)))
