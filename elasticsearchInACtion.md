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
### Relevancy
the degree to which data matches the given query
### Full-text search
technique to search specific phrases within the entire data rather than looking for it in specific fields or sections; doesn't depend on meta data
### Inverted Index
general purpose data structure which maps contents to their location; enable efficient loookups for where specific terms or elements occur within a dataset
### Elastic Stack
- elasticsearch
- logstash
    - open source data processing engine
    - processes data after extracting it from different sources
    - usually transfers or enrichs data while processing it
    - sends data to a variety of target destinations after processing it
    - can be looked at as a real-time data-ingestion pipline due to its architecture
- beats
    - single purposed data consumption component
    - loads data from different external systems & pump it into Elasticsearch
    - requires its agents to be installed on the host machine (or VM)
- kibana
    - multi-purpose web interface for the stack
### Consistency Types
- strong
    - deosn't provide immediate data consistency amongst multiple nodes
    - guarantees consistency after enough time has passed
    - can work with huge loads of CRUD operations
- eventual
    - offers immediate data consistency
    - becoms slow under heavy loads of CRUD operations