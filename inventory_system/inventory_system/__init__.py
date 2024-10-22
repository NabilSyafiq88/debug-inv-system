from django.db.models import CharField
from .lookups import CaseInsensitiveExact

CharField.register_lookup(CaseInsensitiveExact)