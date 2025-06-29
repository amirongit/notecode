# Keycloak Authorization Services
## Authorization Services Overview
### Mechanisms
- ABAC (Attribute Based Access Control)
- RBAC (Role Based Access Control)
- UBAC (User Based Access Control)
- CBAC (Context Based Access Control)
- Rule Based Access Control
- Time Based Access Control
### Disadvantages of RBAC
- change is hard due to coupling roles W/ resources
- small domain changes lead to deep architectural changes
- lack of context
### Terminology
#### Resource Server
serves protected resources & is capable of accepting & responding to requests
usually rely on some kind of information to decide whether access should be granted
#### Resource
part of the assets of an application being protected
#### Policy
determines the conditions that must be satisfied to grant access to a resource
#### Scope
bounded extent of access that is possible to perform on a resource
usually indicates what can be done to given resource
#### Role
represents types or categories of users
#### Permission
associates resources with policies in order to authorize
## Managing Resource Servers
### Creating Resource Servers
a client is created with authorization enabled
## Managing Policies
### Negative logic
determines if the result should be negated
### Decision Strategies
#### Unanimous
all of permissions must evaluate to positive to grant access
#### Affirmative
one of the non required permissions must evaluate to positive to grant access
#### Consensus
the number of positive permission evaluations must be greater than the negative ones to grant access
### User Based Policy
permits set of users
### Role Based Policy
permits set of roles
roles can be flagged as required
### JavaScript Based Policy
provides the ability to write complext authorization logic using a JavaScript interface
### Time Based Policy
provides the ability to define time based conditions for permissions
### Aggregated Policy
aggregates multiple policies
### Client Based Policy
permits set of clients
### Group Based Policy
permits set of groups & their hierarchies
### Client Scope Based Policy
permits set of client scopes
## Managing Permissions
### Resource Based Permission
permits set of resources or resource types
### Scope Based Permission
permits set of scopes of a resource or resource type