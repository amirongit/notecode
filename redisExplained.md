# Redis Explained


## Strings

- binary-safe, numerical values & strings
- EXISTS, DEL & SET & GET, TTL, INCR & INCRBY commands
- EX option

## Streams

- an append-only like data structure whose items are immutable, scheme-less, ordered & identified by an id
- XADD, XRANGE & XREVRANGE, XREAD, XTRIM & XLEN commands
- generation of a unique id for each item with *
- COUNT option
- representation of the highest & lowest timestamps with + & -

## Lists

- a sequence of strings
- RPUSH, LPUSH, RPOP, LPOP, LRANGE & LLEN commands

## Sets

- an on-ordered collection of unique strings which supports standard set operations
- SADD & SCARD, SISMEMBER & SINTER & SREM commands

## Sorted sets

- an ordered collection of unique items (which of each associated with an score)
- ZADD, ZINCRBY, ZSCORE, ZRANGE & ZREVRANGE, ZRANK & ZREVRANK COMMANDS
- WITHSCORE option

## Hashes

- a collection of mutable scheme-less key value pairs
- HSET & HDEL, HINCRBY, HGET & HMGET & HGETALL commands
