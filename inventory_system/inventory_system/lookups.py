from django.db.models import Lookup
from django.db.models.functions import Lower

class CaseInsensitiveExact(Lookup):
    lookup_name = 'iexact'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return f"LOWER({lhs}) = LOWER({rhs})", params