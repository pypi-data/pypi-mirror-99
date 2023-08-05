# Serialized Interface Library

https://pypi.org/project/serialized-data-interface/

This libraries enables its user to create serialized and validated Juju Operator interfaces.

An interface Schema will be defined through YAML e.g:

```
type: object
properties:
  service:
    type: string
  port:
    type: number
  access-key:
    type: string
  secret-key:
    type: string
```

When our charms interchange data, this library will validate the data through the schema on both ends.

# Real World Example

**** Minio with Provider Interface: https://github.com/DomFleischmann/charm-minio/tree/argo-relation
* Argo Controller with Requirer Interface: https://github.com/DomFleischmann/argo-operators/tree/operator-v2.3.0/operators/argo-controller

# TODO

* Currently only provides data to App relations, should also support unit relations.
