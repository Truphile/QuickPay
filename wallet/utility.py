import random
import re

from django.db.models.query_utils import refs_expression


def generate_account_number():
   return "44" + str(random.randrange(000000,999999))

def generate_reference_id():
   number = random.randint(100000,999999)
   return "NKY" + str(number)