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
### Full-Text Search
technique to search specific phrases within the entire data rather than looking for it in specific fields or sections; doesn't depend on meta data
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
logical bucket which is dedicated to collect similar data (doesn't enforce schema)
### APIs
some resources are as follow
- index
- documents ("_doc" is a generic pointer to the single document type an index is able to store)
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
- used to perform full-text search on a single field
- logical operator is indicated by the `operator` parameter (defaults to "OR")
- number of allowed misspells is indicated by `fuzziness` parameter
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
#### Multi Match
- used to perform full-text search on multiple fields
- fields can be boosted by their name being appended with `^<boost-factor>`
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
#### Search Phrase
- used to search for a sequence of words in an exact order
- number of missing words in the given phrase can be indicated by `slop` parameter
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
### Term-Level Queries
- used to query precise values such as numbers, dates, ranges & IP addresses in structured data
- produces binary results, meaning that items either match the query or don't
#### Prefix
works like match query; used to search with shortend version of words
```
GET <indices>/_search
{
    "query": {
        "match_phrase_prefix": {
            <field>: <prefix>
        }
    }
}
```
#### Term
used to search for exact non-textual structured values
```
GET <indices>/_search
{
    "query": {
        "term": {
            <field>: {
                "value": <value>
            }
        }
    }
}
```
#### Range
used to search for values that match given range
```
GET <indices>/_search
{
    "query": {
        "range": {
            <field>: {
                "lt": <less-than>,
                "lte": <less-than-or-equal>,
                "gt": <greater-than>,
                "gte": <greater-than-or-equal>
            }
        }
    }
}
```
### Compound Queries
provides a mechanism to combine leaf queries in order to build complex queries
#### Leaf Query
looks for specific values in specific fields; can be used by itself
#### Boolean
used to create sophisticated query logic; consists of four optional clauses made of leaf queries
- must
    - all leaf queries match (matches contribute to relevancy score)
- should
    - one of leaf queries matches (matches contribute to relevancy score)
- must not
    - non of leaf queries match (matches don't contribute to relevancy score)
- filter
    - all leaf queries match (matches don't contribute to relevancy score)
<!---->
```
GET <indices>/_search
{
    "query": {
        "bool": {
            "must": <leaf-queries>,
            "must_not": <leaf-queries>,
            "should": <leaf-queries>,
            "filter": <leaf-queries>
        }
    }
}
```
### Aggregations
used to provide analytics & high level data
#### Metric
simple aggregations like "avg", "sum", "min", "max", "stats" & "extended_stats"
```
GET <indices>/_search
{
    "aggs": {
        <name>: {
            <aggregation-type>: {
                "field": <field>
            }
        }
    }
}
```
#### Bucket
segregates data by intervals into buckets; useful for building visualizations
#### Pipeline
aggregations that work on the output of other aggregations
## Architecture
### The Building Blocks
#### Documents
- basic unit of information in "json" form
- each field is analyzed for faster searches & analytics
- storing multiple types of documents in a single index was supported prior to v5.x
    - since v7.0, "_doc" is the generic single document type an index is able to store
    - this was forced by lucene's inability to define multiple fields with a common name but different data type on each index
#### Indices
- logical connections between similar documents
- documents of an index share the same mapping
    - definition of the schema of documents
- composed of shards
    - indices have a primary & a replica shard by default
- can either exist on a single node or be distributed in a cluster
#### Data Streams
- specific type of extended alias
- templates are used to create associated indices in an interval
    - each index indicates an specific range in time
- write operations execute on the last (current) index
- read operations execute on all indices
#### Shards & Replicas
- shards
    - software components that hold some amount of data
    - physical instances of lucene
        - high performance full-text search engine
    - usually distributed across a cluster for availability & failover
- replicas
    - duplicated copies of primary shards
    - allow redundancy
    - can accept read requests in order to balance heavy loads in the cluster
    - usually don't share the same location with their primary shard
#### Nodes & Clusters
- nodes
    - instances of elasticsearch server
    - host sets of shards & replicas
- clusters
    - collections of nodes
    - can be in one of three health states
        - red
            - not all shards are assigned & ready
        - yellow
            - shards are assigned & ready, but replicas aren't
        - green
            - shards & replicas are assigned & ready
- node roles
    - each role makes a node take specific responsibilities
        - master: cluster management
            - doesn't participate in CRUD operations
            - knows the location of each document
        - data: document persistence & retrieval
            - I/O intensive
        - ingest: transformation of data before indexing
        - coordination: handling client requests (default role)
            - taken on by all nodes as an additional role
            - nodes with only this specific role can act like a load balancer
        - ...
### Inverted Indices
- data structure which maps tokens to containing documents & their frequency of repetition
- enables full-text search
### Relevancy
#### Relevancy Score
positive floating-point number which indicates how relevant a particular result is to the query
#### Relevancy Algorithms
configured per field
- TF-IDF
    - term frequency
        - number of times the search word appears in an specific field of a document
    - inverse document frequency
        - number of times the search word appears across the whole set of documents
    - assignes weight terms based on their TF & IDF
    - terms with more TF & less IDF are considered to be more relevant
- BM25 (Best Matching 25)
    - default relevancy algorithm
    - improvement over TF-IDF
    - prevents terms with high TF from receiving excessively high scores
    - employs document length normalization to counter the bias towards longer documents
- ...
### Routing Algorithm
determines exactly one primary shard for a document as its location (in the context of indices)
```
hash(document.id) % number-of-primary-shards
```
changing number of shards would break this for existing documents, reindexing is done in this situation
### Scaling
#### Scaling Up (Vertical Scaling)
- the process of adding computational resources to the currently existing units of computation
    - like CPU & RAM
- usually causes downtime due to hardware upgradation
#### Scaling Out (Horizontal Scaling)
- the process of adding units of computation to a farm or cluster
    - like VMs or nodes
- doesn't cause downtime
- the process of distributing data among new nodes begins instantly
## Mapping
### Overview Of Mapping
- the process of developing a definition of the schema which represents fields & their associated data types of a document
- elasticsearch expects a single mapping per index which tells it how to treat each field of its documents
### Dynamic Mapping
- the process in which elasticsearch implicitly derives an schema definition from a document for an index
- usually happens when a document is indexed without an schema definition up front
#### Limitations Of Dynamic Mappings
data type of each field is derived based on the value of the first indexed document; therefore, elasticsearch is unable to<br/>
determine the correct schema if a broader prespective is needed to do so
### Explicit Mapping
#### Mapping Using The Indexing API
an schema definition is created simultaneously with its index using "create index" API
```
PUT <index>
{
    "mappings": {
        "properties": {
            <field>: {
                "type": <data-type>,
                <parameter>: <value>
            }
        }
    }
}
```
#### Mapping Using The Mapping API
used to update schema definitions of already existing indices
```
PUT <index>/_mapping
{
    "properties": {
        <field>: {
            "type": <data-type>,
            <parameter>: <value>
        }
    }
}
```
#### Modifying Existing Fields Is Not Allowed
operational indidces with data fields are considered live; modifying the schema definition of these indices will cause wrong<br/>
search results, thus, prohibited; reindexing is done in this situation
#### Type Coercion
the process of casting a value in the format of another data type to the desired data which is in the schema definition
### Data Types
every field can have one or more associated data types
- simple types
    - common data types which represent basic & primitive values
    - like text, boolean, long, date, double & binary
- complex types
    - created by composing additional types; similar to compound or container types in programming languages
    - can be flattened or nested
    - like object, nested, flattened & join
- specialized types
    - used for specialized cases such as geolocation & IP addresses
    - like geo_shape, geo_point, ip & range types like date_range & ip_range
<!---->
schema definition is retrieved using mapping API
```
GET <indices>/_mapping
```
### Core Data Types
#### The Text Data Type
- unstructured full-text data
- values of this data type are analyzed before persistence
    - analyzers enrich, enhance & transform data into internal data structures
    - stemmers can be used to reduce tokens & words to their root
    - this is done so the values can be queried more easily
#### The Keyword Data Types
- structured data
- can't be used in range queries
- queried in binary manner (no relevancy score)
- values get persisted as they are
#### Numberic Data Types
- integer types

|name|signed|size|
|-|-|-|
|byte|+|8bit|
|short|+|16bit|
|integer|+|32bit|
|long|+|64bit|
|unsigned long|-|64bit|

- floating-point types

|name|size|
|-|-|
|float|32bit|
|double|64bit|
|half float|16bit|
|scaled float|64bit|

#### The Range Data Types
- structured data
- represent lower & upper bound of a field
- defined by operators suchs as "lt", "lte", "gt" & "gte"
### Advanced Data Types
#### The Geo Point Data Type
- represents a single geographical point
- can be queried using "get_bounding_box"
    - takes two geo points to form a boxed area
    - searches for points inside the area
```
GET indices/_search
{
    "query": {
        "geo_bounding_box": {
            <field>: {
                "top_left": {
                    "lat": <latitude>,
                    "lon": <longitude>
                },
                "top_right": {
                    "lat": <latitude>,
                    "lon": <longitude>,
                }
            }
        }
    }
}
```
#### The Object Data Type
- hierarchical structured data
- inner properties are flattened before persistence
    - this causes them to lose their collective identity implied by each object
- flattened properties can be accessed using `<parent>.<child>` syntax in queries
#### The Nested Data Type
- specialized form of object
- maintains collective identity of properties implied by each object
#### The Flattened Data Type
- data held in subfields with keyword data type
- subfields aren't defined in the schema definition & used on an ad hoc basis
- no analyzation happens when documents get persisted
    - this makes writing operations cheap
### Fields With Multiple Data Types
additional "fields" key can be provided in order to store desired fields using multiple data types
```
PUT <index>
{
    "mappings": {
        "properties": {
            <field>: {
                "type": <data-type>,
                <parameter>: <value>,
                "fields": {
                    <field-as-data-type>: {
                        "type": <data-type>,
                        <parameter>: <value>,
                    }
                }
            }
        }
    }
}
```
fields as additional data types are accessed by "<field>.<field-as-data-type>" syntax in queries
## Working With Documents
### Indexing Documents
#### Document APIs
- document identifiers
    - unique identifier associated to documents for their lifetime
    - "PUT" method is used when identifier is provided by user
        - `PUT <index>/_doc/<identifier>`
    - "POST" method is used when identifier is expected to be generated
<!-- 154, FIRST LINE OF PAGE -->
