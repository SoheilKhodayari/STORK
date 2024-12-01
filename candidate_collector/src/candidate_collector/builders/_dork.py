from ._base import QueryBuilder

class DorkQueryBuilder(QueryBuilder):

    def __init__(self, domain):
        super().__init__(domain)

    def build(self):
        query_parts = []
    
        # Restrict query to specific domain
        domain_query = f"site:{self.domain}"
        query_parts.append(domain_query)

        # Build query for key requirments being followed by string starting with https
        prepared_key_requirements = [f'"allinurl:{key}=http"' for key in self.key_requirements]
        key_query = f"{' OR '.join(prepared_key_requirements)}"
        query_parts.append(f"({key_query})")

        if len(self.value_requirements) > 1:
            value_query = f"allinurl:({'|'.join(self.value_requirements)})"
            query_parts.append(f'"{value_query}"')
        elif len(self.value_requirements) == 1:
            value_query = f'"allinurl:{list(self.value_requirements)[0]}"'
            query_parts.append(value_query)

        if len(self.path_excludes):
            prepared_path_excludes = [f'"-allinurl:{path_exclude}"' for path_exclude in self.path_excludes]
            query_parts.append(" AND ".join(prepared_path_excludes))

        return f" AND ".join(query_parts)
