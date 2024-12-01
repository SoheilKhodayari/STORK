# Endpoint Analyzer

This package implements a model to learn endpoints of a set of URLs and a given
domain based on customizable heuristics. It is possible to extend the model on
the fly by providing additional URLs to refine the model. It collects query
parameters along with deduced type information of the query parameters and tries
to analyze existing encodings.


## Sample Code
```python
from pprint import pprint
from endpoint_analyzer import EndpointExtractor

urls = fetch_urls_to_analyze()

extractor = EndpointExtractor(domain)
extractor.train_with(urls)
pprint(extractor.endpoints())

```

*Output*:
```
['example'.'com'/'users'/SIMPLE?,
 'example'.'com'/'account'/'login'?next=PATH:DOUBLE_ULR_ENCODED,
 'example'.'com'/'r'/COMPOSITE?,
 'example'.'com'/'r'/SIMPLE?,
 'example'.'com'/'account'/'register'?url=URL:URL_ENCODED,
 'example'.'com'/NUMBER/NUMBER/NUMBER?,
 'example'.'com'/NUMBER/'videos'/NUMBER?,
 'example'.'com'/SIMPLE?,
 NUMBER.'example'.'com'/NUMBER/'videos'/NUMBER?,
 SIMPLE.'example'.'com'/'primes'/NUMBER?]
```

### Running the examples

- `pip install -e .`
- `python examples/example.py`

### Installation instructions

#### For development

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install requirements.txt`

*Optional:*
- `pip install requirements_dev.txt`
