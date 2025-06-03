# Elasticsearch In Action
## Overview
### Data Flavors
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
### Full-Text Search
technique to search specific phrases within the entire data rather than looking for it in specific fields or sections; doesn't depend on meta data
### Inverted Index
general purpose data structure which maps contents to their location; enable efficient lookups for locations of occurrences of terms or elements
### Elastic Stack
- elasticsearch
- logstash
    - open source data processing engine
    - processes data after extracting it from different sources
    - usually transfers or enrichs data while processing it
    - sends data to a variety of target destinations after processing it
    - can be looked at as a real-time data-ingestion pipeline due to its architecture
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
## Getting Started
### Aggregation Types
- metric
    - calculates statistics or metrics over a set of documents
- bucket
    - groups documents into buckets based on specific criterias
    - allows analyzation of buckets
- pipeline
    - processes the results of other aggregations
    - enables step based calculations
- matrix
    - performs operations on multiple fields simultaneously
- composite
    - creates paginated bucket aggregations
    - allows efficient handling of large datasets by breaking them into smaller pieces
- geo
    - specialized for geospatial data
### Being Schema-Less
when the data store doesn't require a defined schema before storing data
### Index
bucket which is dedicated to collect similar data (doesn't enforce schema)
### APIs
some resources are as follow
- index
- documents (`_doc` is a generic pointer to the single document type an index is able to store)
<!---->
APIs are exposed as a suffix of their corresponding resource; sometimes multiple comma-separated resources on the same level can be used
- components
    - HTTP method (action) (verbs)
    - hostname & port
    - resource
    - request body
<!---->
some elasticsearch APIs allow bodies passed in GET requests
### Query DSL
simple json-based query language provided by elasticsearch which is extensively used in kibana
### Indexing A Document
- HTTP verbs have their own exact meaning
- representation of a document can be anything in json format since elasticsearch is schema-less
### Retrieving Data
#### Number Of Documents
- all documents<br/>
`GET _count/`
- documents of specific indices<br/>
`GET <indices>/_count`
#### Documents Themselves
- single document<br/>
    - with meta data<br/>
    `GET <index>/_doc/<id>` 
    - just the document<br/>
    `GET <index>/_source/<id>` 
- multiple documents (considered a "match_all" query when used without any specification)
```
GET <indices>/_search
{
    "query": {"ids": {"values": <array-of-IDs>}},
    "_source": [<fields>,<boolean>]
}
```
### Full-Text Search
operators are applied between multiple space-separated terms in "value" fields
#### Match
used to perform full-text search on a single field<br/>
logical operator is indicated by the `operator` parameter (defaults to "OR")<br/>
number of allowed misspells is indicated by `fuzziness` parameter<br/>
```
GET <indices>/_search
{
    "query": {
        "match": {
            <field>: {
                "query": <value>,
                "operator": <operator>,
                "fuzziness": <allowed-misspells>
            }
        }
    }
}
```
#### Prefix
works like match query; is term-level; used to search with shortend version of words
#### Multi Match
used to perform full-text search on multiple fields<br/>
fields can be boosted by their name being appended with `^<boost-factor>`
```
GET <indices>/_search
{
    "query": {
        "multi_match": {
            "query": <value>,
            "fields": <fields>
        }
    }
}
```
#### Relevancy Score
"_score" field is a positive floating-point number which indicates how relevant a particular result is to the query
#### Search Phrase
used to search for a sequence of words in an exact order
number of missing words in the given phrase can be indicated by `slop` parameter
```
GET <indices>/_search
{
    "query": {
        "match_phrase": {
            <field>: <phrase>
        }
    "slop": <missing-words>
    }
}
```
<!--2.4 term level queries-->
