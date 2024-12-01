# Candidate Collector

Fetch open redirect candidates from [Waybackmachine](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md) or [Google](https://developers.google.com/custom-search/v1/overview).

This package implements builders for creating queries either in regex format
or dork format. Additionally wrappers for querying the respective databases
are available.

## Examples for query construction

```python
from candidate_collector.builders import RegexQueryBuilder
from candidate_collector.builders import ExpandSymbolsPreprocessor

domain = "example.org"
pre_proc = ExpandSymbolsPreprocessor()
pre_proc.expand("ANY", ".*")

builder = RegexQueryBuilder(domain)
builder.register_preprocessor(pre_proc)

regex = (
    builder.ignore_trailing_slash()
    .require_query_value("/ANY")
    .require_query_value("httpANY")
    .require_query_key("next")
    .require_query_key("redirect")
).build()
print(f"{[regex](regex)}")
```

*Output*:
```
(.*//)([^/]*?example.org)(/.*)?(\?(.*(?:(?<=&|\?)(?:next|redirect)(?:=|&|$)|(?<==)(?:/.*|http.*)(?:&|$)).*))
```

### Running the examples

- `pip install -e .`
- `python examples/builder_or.py`

### Installation instructions

#### For development

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install requirements.txt`

*Optional:*
- `pip install requirements_dev.txt`
