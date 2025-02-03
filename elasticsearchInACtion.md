# Elasticsearch In Action
## Overview
### Data flavors
- structured
    - follows an specific schema or format
    - easily searchable
    - binary matching determination logic
- unstructured (or full-text)
    - is unorganized, schema-free & in no specific format
    - non-binary matching determination logic
- semi-structured
    - falls between structured & unstructured data
    - usually is unstructured data with meta-data describing it
#### Relevancy
the degree to which data matches the given query
#### Full-text search
technique to search specific phrases within the entire data rather than looking for it in specific fields or sections; doesn't depend on meta data
#### Inverted Index
general purpose data structure which maps contents to their location; enable efficient loookups for where specific terms or elements occur within a dataset
<!-- popular search engines -->