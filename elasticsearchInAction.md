# Elasticsearch In Action
## Overview
### Data Flavors
- structured
    - follows an specific schema or format
    - easily searchable
    - binary matching determination logic
- unstructured (or full text)
    - is unorganized, schema free & in no specific format
    - non binary matching determination logic
- semi structured
    - falls between structured & unstructured data
    - usually is unstructured data with meta data describing it
### Full Text Search
- technique to search for phrases in entire data rather than specific fields or sections (doesn't depend on metadata)
### Elastic Stack
- elasticsearch
- logstash
    - open source data processing engine
    - processes data after extracting it from different sources
    - usually transfers or enrichs data while processing it
    - sends data to a variety of target destinations after processing it
    - can be looked at as a real time data ingestion pipeline due to its architecture
- beats
    - single purposed data consumption component
    - loads data from different external systems & pump it into Elasticsearch
    - requires its agents to be installed on the host machine (or VM)
- kibana (multi purpose web interface for the stack)
### Consistency Types
- strong
    - offers immediate data consistency
    - becomes slow under heavy loads of CRUD operations
- eventual
    - doesn't provide immediate data consistency amongst multiple nodes
    - guarantees consistency after enough time has passed
    - can work with huge loads of CRUD operations
## Getting Started
### Aggregation Types
- metric (calculates statistics or metrics over a set of documents)
- bucket
    - groups documents into buckets based on specific criterias
    - allows analyzation of buckets
- pipeline
    - processes the results of other aggregations
    - enables step based calculations
- matrix (performs operations on multiple fields simultaneously)
- composite
    - creates paginated bucket aggregations
    - allows efficient handling of large datasets by breaking them into smaller pieces
- geo (specialized for geospatial data)
### Being Schema Less
- when the data store doesn't require a defined schema before storing data
### Index
- logical bucket which is dedicated to collect similar data (doesn't enforce schema)
### APIs
- some resources are as follow
    - index
    - documents ("_doc" is a generic pointer to the single document type an index is able to store)
<!---->
- APIs are exposed as a suffix of their corresponding resource
    - sometimes multiple comma separated resources on the same level can be used
    - components
        - HTTP method (action) (verbs)
        - hostname & port
        - resource
        - request body
<!---->
- some elasticsearch APIs allow bodies passed in GET requests
### [Query DSL](#query-dsl-1)
### [Indexing A Document](#indexing-documents)
- representation of a document can be anything in json format since elasticsearch is schema less
### Retrieving Data
#### Number Of Documents
- all documents<br/>
    `GET _count`
- documents of specific indices<br/>
    `GET <indices>/_count`
#### Documents Themselves
- [single document](#using-the-single-document-api)
- [multiple documents](#retrieving-multiple-documents)
### Full Text Search
- operators are applied between multiple space separated terms in "value" fields
#### [Match](#the-match-query)
#### [Multi Match](#the-multi_match-query)
#### [Match Phrase](#the-match_phrase-query)
### [Term Level Queries](#term-level-search)
#### [Prefix](#the-prefix-query)
#### [Term](#the-term-query)
#### [Range](#the-range-query)
### [Compound Queries](#compound-queries)
#### [Leaf Queries](#leaf-queries-1)
#### [Boolean](#the-boolean-query)
### Aggregations
- used to provide analytics & high level data
#### Metric
- simple aggregations like "avg", "sum", "min", "max", "stats" & "extended_stats"
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
- segregates data by intervals into buckets
- useful for building visualizations
#### Pipeline
- aggregations that work on the output of other aggregations
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
- documents of an index share the same [schema definition](#mapping)
- composed of shards (one primary & one replica shard by default)
- can either exist on a single node or be distributed in a cluster
#### Data Streams
- specific type of extended alias
- templates are used to create associated indices in an interval
- write operations execute on the last (current) index
- read operations execute on all indices
#### Shards & Replicas
- shards
    - software components that hold some amount of data
    - physical instances of lucene (high performance full text search engine)
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
- clusters (collections of nodes)

|health status|description|
|-|-|
|red|not all shards are assigned & ready|
|yellow|shards are assigned & ready, but replicas aren't|
|green|shards & replicas are assigned & ready|

- node roles (duties assigned to each node)

|role|description|
|-|-|
|master|cluster management; doesn't participate in CRUD operations|
|data|document persistence & retrieval (IO intensive)|
|ingest|transformation of data before indexing|
|coordination|handling client requests (taken on by all nodes as an additional role)|
|...|...|

### Inverted Indices
- data structure which maps tokens to containing documents & their frequency of repetition
- enables full text search
### Relevancy
#### Relevancy Score
- positive floating point number indicating how relevant results are to query
- alternative to binary matching logic
#### Relevancy Algorithms
- configured per field
    - TF-IDF
        - term frequency: number of times the search word appears in an specific field of a document
        - inverse document frequency: number of times the search word appears across the whole set of documents
        - assignes weight terms based on their TF & IDF
        - terms with more TF & less IDF are considered to be more relevant
    - BM25 (Best Matching 25) (default)
        - improvement over TF-IDF
        - prevents terms with high TF from receiving excessively high scores
        - employs document length normalization to counter the bias towards longer documents
    - ...
### Routing Algorithm
- determines exactly one primary shard for a document as its location (in the context of indices)<br/>
    `hash(document.id) % <number-of-primary-shards>`
- changing number of shards would break this for existing documents, reindexing is done in this situation
### Scaling
#### Scaling Up (Vertical Scaling)
- the process of adding computational resources to the currently existing units of computation (like CPU & RAM)
- usually causes downtime due to hardware upgradation
#### Scaling Out (Horizontal Scaling)
- the process of adding units of computation to a farm or cluster (like VMs or nodes)
- doesn't cause downtime
- the process of distributing data among new nodes begins instantly
## Mapping
- field are able to hold zero to more values; all data types are array of "T" by default
### Overview Of Mapping
- the process of developing a definition of the schema which represents fields & their associated data types of a document
- elasticsearch expects a single mapping per index which tells it how to treat each field of its documents
### Dynamic Mapping
- the process in which elasticsearch implicitly derives an schema definition from a document for an index
- usually happens when a document is indexed without an schema definition up front
#### Limitations Of Dynamic Mappings
- data type of each field is derived based on the value of the first indexed document
- correct schema can't be determined if broader prespective is needed
### Explicit Mapping
- mapping property object
    ```
    {
        "type": <data-type>,
        <parameter>: <value>
    }
    ```
#### Mapping Using The Indexing API
- schema definition is created simultaneously with its index using "create index" API
    ```
    PUT <index>
    {
        "mappings": {
            "properties": {
                <field>: <mapping-property-object>
            }
        }
    }
    ```
#### Mapping Using The Mapping API
- used to update schema definitions of already existing indices
    ```
    PUT <index>/_mapping
    {
        "properties": {
            <field>: <mapping-property-object>
        }
    }
    ```
#### Modifying Existing Fields Isn't Allowed
- operational indidces with data fields are considered live
- modifying the schema definition of live indices will cause wrong search results & is prohibited
- reindexing is done in this situation
#### Type Coercion
- process of casting values in form of another data type to desired data format specified in schema definition
### Data Types
- every field can have one or more associated data types
- simple types
    - common data types which represent basic & primitive values
    - like text, boolean, long, date, double & binary
- complex types
    - created by composing additional types
    - similar to compound or container types in programming languages
    - like object, nested, flattened & join
- specialized types
    - used for specialized cases such as geolocation & IP addresses
    - like geo_shape, geo_point, ip & range types like date_range & ip_range
<!---->
- schema definition is retrieved using "mapping" API<br/>
    `GET <indices>/_mapping`
### Core Data Types
#### The Text Data Type
- unstructured full text data
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

- floating point types

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
    - takes two geo points to form a boxed area
    - searches for points inside the area
#### The Object Data Type
- hierarchical structured data
- inner properties are flattened before persistence (this causes them to lose their collective identity implied by each object)
- flattened properties can be accessed using "<parent>.<child>" syntax in queries
#### The Nested Data Type
- specialized form of object
- maintains collective identity of properties implied by each object
#### The Flattened Data Type
- data held in subfields with keyword data type
- subfields aren't defined in the schema definition & are used on an ad hoc basis
- no analyzation happens when documents get persisted (this makes writing operations cheap)
### Fields With Multiple Data Types
- "fields" parameter in ["mapping-property-object"](#explicit-mapping) is used for additional data types
- additional data types are accessed by "<field>.<field-as-data-type>" syntax in queries
## Working With Documents
### Indexing Documents
#### Document APIs
- document identifiers
    - unique identifier associated to documents for their lifetime
    - documents are updated or overwritten in case of existence
    - "PUT" method is used when identifier is provided by user<br/>
        `PUT <index>/_doc/<identifier>`
    - "POST" method is used when identifier is expected to be generated ("identifier" is optional)<br/>
        `POST <index>/_doc/<identifier>`
<!---->
- avoiding overwrites
    - "_doc" is replaced by "_create"
    - indicates that the document should be created
    - raises error if the document already exists
#### Mechanics Of Indexing
1. routing algorithm is used to determine document's location
2. chosen shard holds the given document in its heap memory buffer (this is done to avoid frequent IO operations)
3. after refresh signal is issued by lucene
    - buffered documents will be collected into segments
    - segments contain inverted indices & documents themselves
    - segments are immutable
4. data is written to the FS cache & then commited to the physical disk (documents can be searched & accessed in this step)
5. after formation of three segments
    - peer segments are merged together
    - this happens recursively until a certain point (which idk about)
<!---->
- delete operation marks documents to be removed later, as segments are immutable (this probably happens in the process of segments being merged)
#### Customizing The Refresh Process
- server side
    ```
    PUT <indices>/settings
    {
        "index": {
            "refresh_interval": <refresh-interval>
        }
    }
    ```
- client side ("refresh" query parameter)

|parameter value|description|
|-|-|
|false|doesn't force the refresh operation (default)|
|true|forces the refresh operation|
|wait_for|blocks the request & returns after a refresh operation happens|

- buffered documents may be lost in the case of server breakdown before successfull refresh operation
- there is a direct (positive) correlation between refresh rate & weight of IO operations
- there is an indirect (negative) correlation between refresh rate & the possibality of data loss
### Retrieving Documents
#### Using The Single Document API
- data & metadata retrieve<br/>
    `GET <index>/_doc/<identifier>`
- existence check<br/>
    `HEAD <index>/_doc/<patterns>`
#### Retrieving Multiple Documents
- [from single index](#the-ids-query)
- from multiple indices
    ```
    GET _mget
    {
        "docs": [
            {
                "_index": <index>,
                "_id": <identifier>
            }
        ]
    }
    ```
### [Manipulating Responses](#manipulating-results)
### Updating Documents
- script object
    ```
    {
        "source": <script>,
        "params": <parameters>,
        "lang": <language>
    }
    ```
#### Document Update Mechanics
- procedure of updating documents (replacing documents with newer version of themselves)
    1. fetch
    2. modify
    3. increment version
    4. mark old one for deletion
    5. index new one (reindex)
#### The "_update" API
```
POST <index>/_update/<identifier>
{
    "_doc": {
        <field>: <value>
    }
}
```
- values are replaced
#### Scripted Updates
```
POST <index>/_update/<identifier>
{
    "script": <script-object>
}
```
- document updates based on context & conditions
- context is contained in "ctx" variable
- scripting language
    - `params.<param>`
    - `ctx._source.<field>`
    - `ctx._source.remove(<field>)`
    - `ctx._source.<array-field>.add(<value>)`
    - `ctx._source.<array-field>.remove(<value>)`
    - `ctx._source.<array-field>.indexOf(<value>)`
    - `if (<condition>) {<instruction>} else {<instruction>}`
- anatomy of script-object

|part|description|
|-|-|
|source|conditions, expressions, assignments & modifications|
|lang|expression language (defaults to "painless")|
|params|enables passing data to script dynamically|

#### [Replacing Documents](#document-apis)
#### Upserts
- meaning update if exists insert otherwise
    ```
    POST <index>/_update/<identifier>
    {
        "script": <script>,
        "upsert": <document>
    }
    ```
#### Updates As Upserts
```
POST <index>/_update/<identifier>
{
    "doc": <document>,
    "doc_as_upsert": <boolean>
}
```
- setting "doc_as_upsert" to "true" causes "document" to be saved if it doesn't exist already
#### Updating With A Query
- updating set of documents matching specific criteria
    ```
    POST <index>/_update_by_query
    {
        "query": <query>,
            "script": <script>
    }
    ```
- failures will be logged but won't stop the operation
- retries, logs & batch sizes can be configured
### Deleting Documents
#### Deleting With An ID
- `DELETE <index>/_doc/<identifier>`
- causes "_version" to be increased if done successfully
#### Deleting By Query
- deleting set of documents matching specific criteria
    ```
    POST <index>/_delete_by_query
    {
        "query": <query>
    }
    ```
### Working With Documents In Bulk
- request body
    ```
    POST _bulk
    {<operation>: <metadata>}
    <document>
    ```
- metadata<br/>
    `{"_index": <index>, "_id": <identifier>}`
- operation
    - "index"
    - "delete"
    - "create" (avoids overrides)
    - "update"
- uses "ndjson" instead of "json"
- different components could be moved or omitted based on contextual conditions
### Reindexing Documents
- moving documents between two indices
    ```
    POST _reindex
    {
        "source": {"index": <index>},
        "dest": {"index": <index>},
    }
    ```
## Indexing Operations
- sets of configurations of indices
    - settings
    - mappings
    - aliases
- components of indices
    - aliases
    - settings
    - schema mappings
### Creating Indices
#### Indices With Custom Settings
- index settings
    - static
        - applied in the process of creation
        - can't be changed on operational indices
    - dynamic (able to change on live indices)
- creating indices with explicit non default settings
    ```
    PUT <index>
    {
        "settings": {
            <setting>: <value>
        }
    }
    ```
- updating dynamic settings of indices
    ```
    PUT <index>/_settings
    {
        "settings": {
            <setting>: <value>
        }
    }
    ```
- getting settings of indices ("setting" is optional)<br/>
    `GET <patterns>/_settings/<setting>`
#### Index With Aliases
- "is_write_index" configuration is used to mark indices as writable through aliases (should be set to true on at least one index when creating aliases for multiple indices)
- aliases (alternate names given to indices)
- creating aliases
    - using "index" API
        ```
        PUT <index>
        {
            "aliases": {
                <alias>: {
                    "is_write_index": <is-write-index>
                }
            }
        }
        ```
    - using "alias" API<br/>
        `PUT <patterns>/_alias/<alias>`
- multiple aliasing operations
    - actions
        ```
        {
            <operation>: {
                "index": <index>,
                    "indices": <indices>,
                    "alias": <alias>,
                    "is_write_index": <is-write-index>
            }
        }
        ```
    - operation
        - add
        - remove
    - _aliases API combines adding & removing aliases as well as deleting indices
        ```
        POST _aliases
        {
            "actions": [<actions>]
        }
        ```
### Reading Indices
#### Reading Public Indices
- component
    - "_settings"
    - "_mapping"
    - "_alias"
- fetching details of indices, including settings, schema mappings & aliases ("field" is optional; should be specific field of mentioned component)<br/>
    `GET <patterns>/<component>/<field>`
#### Reading Hidden Indices
- indices with "." as the first character of their name
- will be reserved for system related stuff in future versions
### Deleting Indices
- deleting indices<br/>
    `DELETE <patterns>`
- deleting aliases<br/>
    `DELETE <patterns>/_alias/<alias>`
### Closing & Opening Indices
#### Closing Indices
- indices are put on hold for any operation (including read & write)<br/>
    `POST <index>/_close`
#### Opening Indices
`POST <index>/_open`
### Index Template
- templates with pre defined index components & an index pattern
- applied to inidices whos name match the index pattern (when being created)
- explicit index components begin set override templates
- template priorities are used when overlapping happens
- composable templates
    - able to compose multiple component templates
    - able to define index components on their own
- component templates
    - reusable set of pre defined index components
    - able to be used by multiple composable templates
    - can't be used on its own
#### Creating Composable Templates
```
POST _index_template/<template>
{
    "index_patterns": <patterns>,
    "priority": <priority>,
    "template": {
        "mappings": <mappings>,
        "settings": <settings>,
        "aliases": <aliases>,
    },
    "composed_of": <component-templates>
}
```
#### Creating Component Templates
```
POST _component_template/<component-template>
{
    "template": {
        "mappings": <mappings>,
        "settings": <settings>,
        "aliases": <aliases>,
    }
}
```
### Advanced Operations
#### Splitting An Index
- splitting indices into more shards
- write operations should be disabled on indices before getting splitted
    ```
    PUT <index>/_settings
    {
        "index.blocks.writes": true
    }
    ```
- settings with intention of preparing indices for splitting process must be undone explicitly
- dest shouldn't exist before splitting process
- index components are copied from source to dest if not explicitly set
- number of shards of dest should be multiple of number of shards of source
- using "split" API
    ```
    POST <source-index>/_split/<dest-index>
    {
        "settings": <settings>,
        "mappings": <mappings>,
        "aliases": <aliases>
    }
    ```
#### Shrinking An Index
- shrinking indices into fewer shards
- write operations should be disabled on & shards should be on one single node for indices before getting shrinked
    ```
    PUT <index>/_settings
    {
        "index.blocks.writes": true,
        "index.routing.allocation.require._name": <node>
    }
    ```
- settings with intention of preparing indices for shrinking process must be undone explicitly
- dest shouldn't exist before splitting process
- index components are copied from source to dest if not explicitly set
- number of shards of dest should be factor of number of shards of source
- using "shrink" API
    ```
    POST <source-index>/_shrink/<dest-index>
    {
        "settings": <settings>,
        "mappings": <mappings>,
        "aliases": <aliases>
    }
    ```
#### Rolling Over An Index Alias
- process of making an old index read only & creating new index behind the same alias
- steps
    1. an alias is created
        - value of "is_write_index" is set to true for at least one index
        - index names confirm to pattern "<prefix>-<digits>"
    2. rollover is invoked (can be configured to be automatic)
        - using "rollover" API ("index" is optional)<br/>
            `POST <alias>/_rollover/<index>`
    3. new writable index is created with digits incremented by one
    4. old index is put in read only mode
    5. alias is chaned to point to new index
## Text Analysis
- process of breaking text into tokens & storing them in internal an data structure
- makes query results faster & enables relevance based scoring
### Overview
#### Querying Unstructured Data
- [data flavors](#data-flavors)
- [relevancy](#relevancy)
#### Analyzers To The Rescue
- [text data type](#the-text-data-type)
- full text queries are tokenized in order to match existing tokens
### Analyzer Modules
- software components used to tokenize & normalize full text data
#### Tokenization
- process of chopping full text data into small sections called tokens by following certain rules (delimiters, ignored parts, etc...)
#### Normalization
- process of modification, enrichment & transformation of tokens
    - reducing tokens to their root word (stemming)
    - finding synonyms
    - removing stop words
    - making tokens lowercase
#### Anatomy Of An Analyzer
- components of analyzer modules
    - character filters
        - remove unwanted characters across data
        - able to match & replace characters using regex patterns
        - there can be zero to multiple instance of them
    - tokenizers
        - handle tokenization
        - there should be one single instance of them
    - token filters
        - handle normalization
        - able to change case of, find & add synonyms to & replace root words with tokens
        - there can be zero to multiple instance of them
#### Testing Analyzers
- "_analyze" API (fields other than "text" are optional)
    ```
    GET _analyze
    {
        "text": <text>,
        "analyzer": <analyzer>,
        "tokenizer": <tokenizer>,
        "filter": <filters>
    }
    ```
### Built in Analyzers
- there are built in analyzers
- official documentation would make more sense to read, use & refer to
### Custom Analyzers
- using "setting" object through "create index" API ("char_filter", "tokenizer" & "filter" are optional)
    ```
    put <index>
    {
        "settings": {
            "analysis": {
                "analyzer": {
                    <analyzer>: {
                        "type": "custom",
                        "char_filter": <character-filters>,
                        "tokenizer": <tokenizer>,
                        "filter": <token-filters>
                    }
                },
                "char_filter": {
                    <character-filter>: {
                        "type": <type>,
                        <parameter>: <value>
                    }
                },
                "tokenizer": {
                    <tokenizer>: {
                        "type": <type>,
                        <parameter>: <value>
                    }
                },
                "filter": {
                    <token-filter>: {
                        "type": <type>,
                        <parameter>: <value>
                    }
                },
            }
        }
    }
    ```
- testing custom analyzers using "_analyze" API
    ```
    post <index>/_analyze
    {
        "text": <text>,
        "analyzer": <analyzer>
    }
    ```
### Specifying Analyzers
#### Analyzers For Indexing
- "analyzer" parameter in ["mapping-property-object"](#explicit-mapping) is used to specify field level analyzer
- "analysis.analyzer.default" index setting is used to specify indexl level analyzer
#### Analyzers For Searching
- "search_analyzer" parameter in ["mapping-property-object"](#explicit-mapping) is used to specify field level analyzer for searching purposes
- "analysis.analyzer.default_search" index setting is used to specify indexl level analyzer for searching purposes
- analyzer specification is done in different ways for different types of queries
## Introducing Search
### Overview
- [structured search](#data-flavors) (performed using term level queries)
- [unstructured search](#data-flavors)
### How Does Search Work
1. search request is passed to an available [coordinator](#nodes--clusters) node
2. [data](#nodes--clusters) nodes having applicable shards are determined
3. query is processed by determined nodes on corresponding shards
4. active coordinator merges & sorts results from determined nodes & returns
### Search Fundamentals
#### The "_search" Endpoint
- supported invocation methods

|method|description|
|-|-|
|URI|query is provided as query parameter (discouraged)|
|query DSL|query is wrapped in json object with specific syntax (preferred)|

#### Query vs Filter Context
- execution context

|context|description|
|-|-|
|query|relevancy score is calculated for each result|
|filter|relevancy score isn't calculated|

### Anatomy Of Requests & Responses
#### Search Requests
```
GET <search-criteria>/_search
{
    "query": {
        <query-type>: <query-criteria>
    }
}
```
- "search-criteria" (optional)
    - comma separated indices & aliases
    - if not provided, means all indices of cluster
- "query-criteria" (optional)
    - defines suitable query in regarding "query-type" (optional)
    - includes pagination related properties, included & excluded fields, etc... (all of which is optional)
- "query-type"
#### Search Responses
- "took": time it took coordinator to process request & return response
- "timed_out": if any shards failed to respond (responses of shards are aggregated & returned)
- "shards": number of total, failed, successfull & skipped shards
- "hits": information about query result & result itself
    - "hits": array of results (& usually their meta data)
    - "total": number of results
    - "max_score": highest relevancy score across results
### Query DSL
```
<verb> <endpoint>
{
    "query": <query-object>
}
```
- json based query language
- used for search & analytics
- used to create basic, complex & nested queries
#### Leaf Queries
- queries single set of fields with single operation
- isn't able to combine multiple criteria or queries
- can be taught as atomic unit of queries
### Search Features
#### Pagination
- "size" property is used to determine maximum number of results
- "from" property is used to offset results
#### Highlighting
#### Explaining Relevancy Score
#### Sorting
- sort object
    ```
    {
        <field>: {
            "order": <order>
        }
    }
    ```
- order
    - "asc"
    - "desc"
- results are sorted descendingly by relevancy score by default
- "sort" property is used to manage sorting (expects array of "sort-object"s or field names)
    - relevancy score isn't calculated if "_score" isn't one of the items in "sort" property
    - "track_scores" property is used to force calculation of relevancy score
#### Manipulating Results
- script field object
    ```
    {
        <field>: {
            "script": <script-object>
        }
    }
    ```
- source object
    ```
    {
        "includes": <fields>,
        "excludes": <fields>
    }
    ```
- "_source" property is used to suppress or limit returned fields
    - boolean is passed to suppress or allow whole document
    - array of field names is passed to specify included fields
    - source-object is passed to specify included & excluded fields
    - is able to work with wildcards
- "fields" property is used to specify present fields (expects array of field names)
    - causes fields to return inside arrays
    - is able to work with wildcards
- "script_fields" property is used to generate fields on the fly (expects script-field-object)
#### Searching Across Indices & Data Streams
- index boost object
    ```
    {
        <index>: <boost>
    }
    ```
- "indices_boost" property is used to boost or nerf results by their indices (expects array of "index-boost-object"s)
## Term Level Search
### Overview Of Term Level Search
- designed to work with [structured data](#data-flavors)
- results are determined in binary manner
- queried values usually aren't analyzed before being compared against text fields
### The Term Query
- term query object ("boost" is optional)
    ```
    {
        "term": {
            <field>: {
                "value": <value>,
                "boost": <boost>
            }
        }
    }
    ```
- fetches documents whose value of "field" equals to "value"
### The Terms Query
- terms query object
    ```
    {
        "terms": {
            <field>: <field-values>
        }
    }
    ```
    - values array "field values"<br/>
        `<values>`
    - term lookup "field values"
        ```
        {
            "index": <index>,
            "id": <identifier>,
            "path": <remote-field>
        }
        ```
- fetches documents whose value of "field" is present in "values"
#### The Term Lookup Query
- modification of terms query
- used to build queries based on obtained values from other documents (possibly of other indices)
### The IDs Query
- ids query object
    ```
    {
        "ids": {
            "values": <identifiers>
        }
    }
    ```
- fetches documents whose identifier is present in "identifiers"
- terms query can also be used with "_id" field
### The Exists Query
- exists query object
    ```
    {
        "exists": {
            "field": <field>
        }
    }
    ```
- fetches documents which have "field" as one of their fields
### The Range Query
- range query object
    ```
    {
        "range": {
            <field>: {
                <operator>: <value>
            }
        }
    }
    ```

|operator|description|
|-|-|
|lt|less than|
|lte|less than or equal to|
|gt|greater than|
|gte|greater than or equal to|

- fetches documents whose value of "field" satisfies conditions regarding "operator" & "value"
### The Wildcard Query
- wildcard query object
    ```
    {
        "wildcard": {
            <field>: {
                "value": <pattern>
            }
        }
    }
    ```

|special character|description|
|-|-|
|?|exactly one character|
|*|zero or more characters|

- fetches documents whose value of "field" matches "pattern"
### The Prefix Query
- prefix query object
    ```
    {
        "prefix": {
            <field>: {
                "value": <value>
            }
        }
    }
    ```
- fetches documents whose value of "field" starts with "value"
#### Speeding Up Prefix Queries
- index prefix object
    ```
    {
        "min_chars": <min-chars>,
        "max_chars": <max-chars>
    }
    ```

|clause|default value|
|-|-|
|min_chars|2|
|max_chars|5|

- "index_prefixes" parameter in ["mapping-property-object"](#explicit-mapping) is used in order to index prefixes when indexing documents (expects "index-prefix-object")
### Fuzzy Queries
- fuzzy query object
    ```
    {
        "fuzzy": {
            <field>: <value>,
            "fuzziness": <fuzziness>
        }
    }
    ```
- fetches documents whose value of "field" is similar to "value"
- levenshtein distance algorithm is used to calculate similarity regarding "fuzziness"
## Full Text Searches
- designed to work with [unstructured data](#data-flavors)
- results are determined in non binary manner
- queried values usually are analyzed before being compared against text fields
### Overview
- results are determined using [relevancy algorithms](#relevancy-algorithms)
- precision & recall are used to evaluate results of search query (inversely proportional)

|determination|description|
|-|-|
|true positive|correctly included|
|false positive|incorrectly included|
|false negative|incorrectly excluded |
#### Precision
- portion of retrieved data relevant to search query (quality of results)<br/>
    `true postivies / (true positives + false positives)`
#### Recall
- portion of relevant data retrieved (quantity of results)<br/>
    `true positives / (true positives + false negatives)`
### The "match_all" Query
- match_all query object
    ```
    {
        "match_all": {
            "boost": <boost>
        }
    }
    ```
- used as default query when query type isn't specified for ["_search" API](#the-_search-endpoint)
- 100% recall
- fetches all available documents
### The "match_none" Query
- match_none query object
    ```
    {
        "match_none": {}
    }
    ```
- doesn't fetch any document
### The Match Query
- match query object
    ```
    {
        "match": {
            <field>: {
                <parameter>: <value>
            }
        }
    }
    ```

|parameter|description|possible values|default|
|-|-|-|-|
|query\*|text to be queried|
|operator|logical operator used to determine matching results|AND, OR|OR|
|analyzer|used to convert value of "query" into tokens|AUTO, ...|analyzer of "field"|
|fuzziness|allowed number of misspells (levenshtein distance algorithm)|
|minimum_should_match|minimum number of matched tokens|

- fetches documents whose value of "field" contains tokens of value of "query"
### The "match_phrase" Query
- match_phrase query object
    ```
    {
        "match_phrase": {
            <field>: {
                "query": <phrase>,
                "slop": <slop>,
                "analyzer": <analyzer>
            }
        }
    }
    ```

|clause|description|
|-|-|
|slop|number of allowed absent tokens|
|analyzer|analyzer used to convert "phrase" into tokens|

- fetches documents whose value of "field" contains tokens of "phrase" in the same order
### The "multi_match" Query
- multi_match query object
    ```
    {
        "multi_match": {
            "query": <query>
            "fields": <fields>
        }
    }
    ```
- fields are boosted by being written like `<field>^<boost>`
- fetches documents having tokens of values of one of "fields" fields matching "query"
## Compound Queries
- used to combine multiple compund or [leaf](#leaf-queries) queries
- clauses are usually joined using logical operators & conditions
- offer complex functionalities suchs as custom scoring, boosting & negating logic
### The Boolean Query
- bool query object
    ```
    {
        "bool": {
            <clause>: <queries>
        }
    }
    ```
    - "minimum_should_match" parameter of bool query object
        - used to set minimum number of wrapped queries which documents must satisfy
        - defaults to 0 when "must" caluse isn't empty
        - defaults to 1 when "must caluse is empty"
    - "_name" parameter of wrapped queries
        - used to name queries
        - if set, result documents will contain name of queries they matched

|clause|logical operator|queries to be matched|execution context|
|-|-|-|-|
|must|AND|all|query|
|must_not|NOT|none|filter|
|should|OR|minimum_should_match|query|
|filter|AND|all|filter|
