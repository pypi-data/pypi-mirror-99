# mnubo SmartObjects Python client


[![Build status](https://travis-ci.com/mnubo/smartobjects-python-client.svg?branch=master)](https://travis-ci.com/mnubo/smartobjects-python-client)
[![PyPI](https://img.shields.io/pypi/v/smartobjects.svg?maxAge=2592000)](https://pypi.python.org/pypi/smartobjects/)

## Quickstart

[comment]: # (Important: leave the HTML in this section)
[comment]: # (quickstart-setup)

<h3>Getting the client library</h3>
<p>The client library is available on <a target="_blank" href="https://pypi.python.org/pypi/smartobjects">PyPy</a>.</p>

<p>The client depends on other libraries:</p>
<ul>
    <li>requests</li>
    <li>tenacity</li>
    <li>pandas (optional)</li>
</ul>

<p>Below is an example of how you can install everything:</p>
<pre>
    <code>
pip install smartobjects requests tenacity pandas
    </code>
</pre>

<p>For more information, visit <a target="_blank" href="https://github.com/mnubo/smartobjects-python-client">GitHub</a>.</p>

<h3>Create a client instance</h3>

<p>The following python code can be used to create an instance:</p>

<pre>
    <code>
key = "<%= clientKey %>"
secret = "<%= clientSecret %>"
url = "<%= url %>"
SmartObjectsClient(key, secret, url)
    </code>
</pre>

[comment]: # (quickstart-setup)


Table of Content
================

[1. Introduction](#1-introduction)

[2. At a glance](#2-at-a-glance)

[3. Requirements](#3-requirements)

[4. Installation & Configuration](#4-installation--configuration)

[5. Usage](#5-usage)

[6. Need help?](#6-need-help)

---

# 1. Introduction

This package provides a simple Python client to connect to mnubo's SmartObjects platform.
It gives access to the most common features of mnubo's REST API. All methods require proper authentication.
The MnuboClient object handles authentication under the hood based on the client_id and client_secret arguments.

Methods such as `create()`, `delete()`, etc, do not return any value. However if anything is invalid or goes wrong, an
exception will be thrown so you know what happened.

See the complete documentation [here](https://smartobjects.mnubo.com/documentation/).


# 2. At a glance

_(optional arguments omitted)_

| Service | Method                                               | Summary                                                                 | Example                                           |
| ------- | ---------------------------------------------------- | ------------------------------------------------------------------------| ----------------------------------------          |
| Owners  | `create(owner)                                     ` | create a new owner                                                      | [simple_workflow.py](examples/simple_workflow.py) |
|         | `update(username, owner)                           ` | update an existing owner                                                |                                                   |
|         | `claim(username, device_id, optional_body)         ` | link an existing object to an existing owner                            | [simple_workflow.py](examples/simple_workflow.py) |
|         | `unclaim(username, device_id, optional_body)       ` | unlink an existing object from an existing owner                        | [simple_workflow.py](examples/simple_workflow.py) |
|         | `batch_claim(claims)                               ` | claim a batch of objects                                                | [simple_workflow.py](examples/simple_workflow.py) |
|         | `batch_unclaim(unclaims)                           ` | unclaim a batch of objects                                              | [simple_workflow.py](examples/simple_workflow.py) |
|         | `create_update(owners)                             ` | create or update a batch of owners                                      |                                                   |
|         | `delete(username)                                  ` | delete an owner                                                         |                                                   |
|         | `owner_exists(username)                            ` | check if an owner exists                                                | [simple_workflow.py](examples/simple_workflow.py) |
|         | `owners_exist(usernames)                           ` | check if a list of owners exist                                         |                                                   |
| Objects | `create(object)                                    ` | create a new smart object                                               | [simple_workflow.py](examples/simple_workflow.py) |
|         | `update(device_id, object)                         ` | update an existing object                                               |                                                   |
|         | `create_update(objects)                            ` | create or update a batch of objects                                     |                                                   |
|         | `delete(device_id)                                 ` | delete an object                                                        |                                                   |
|         | `object_exists(device_id)                          ` | check if an object exists                                               | [simple_workflow.py](examples/simple_workflow.py) |
|         | `objects_exist(device_ids)                         ` | check if a list of objects exist                                        |                                                   |
| Events  | `send(events)                                      ` | send a batch of events tagged with multiple devices                     |                                                   |
|         | `send_from_device(device_id, events)               ` | send an event tagged with a specific device                             | [simple_workflow.py](examples/simple_workflow.py) |
|         | `event_exists(event_id)                            ` | check if an event exists                                                |                                                   |
|         | `events_exist(event_ids)                           ` | check if list of events exist                                           |                                                   |
| Search  | `search(query)                                     ` | performs a search in the platform with the provided JSON query (MQL)    | [simple_workflow.py](examples/simple_workflow.py) |
|         | `validate_query(query)                             ` | validates a MQL query                                                   | [simple_workflow.py](examples/simple_workflow.py) |
|         | `get_datasets()                                    ` | retrieves the list of datasets available for this account               | [simple_workflow.py](examples/simple_workflow.py) |
| Model   | `export()                                          ` | fetches the model in the current zone                                   | [model_workflow.py](examples/model_workflow.py)   |
|         | `get_timeseries()                                  ` | fetches the timeseries in the current zone                              |                                                   |
|         | `get_object_attributes()                           ` | fetches the object attributes in the current zone                       |                                                   |
|         | `get_owner_attributes()                            ` | fetches the owner attributes in the current zone                        |                                                   |
|         | `get_event_types()                                 ` | fetches the event types in the current zone                             |                                                   |
|         | `get_object_types()                                ` | fetches the object typesin the current zone                             |                                                   |
| Datalake| `create(dataset)                                   ` | create a new dataset                                                    |                                                   |
|         | `delete(datasetKey)                                ` | delete a dataset                                                        |                                                   |
|         | `list()                                            ` | list all datasets                                                       |                                                   |
|         | `update(datasetKey)                                ` | update an existing dataset                                              |                                                   |
|         | `get(datasetKey)                                   ` | fetch a dataset definition                                              |                                                   |
|         | `add_field(datasetKey, datasetField)               ` | add fields to a dataset                                                 |                                                   |
|         | `update_field(datasetKey, fieldKey, datasetField)  ` | update a dataset field definition                                       |                                                   |
|         | `send(datasetKey, data)                            ` | stream data into a dataset                                              |                                                   |

The API in sandbox and production is mostly the same. Only the modeler API is different in sandbox.
Here are the sandbox only operations that are available on the modeler API:

| Entity             |Method                                                           | Summary                                                                 | Example                                           |
| -------------------|---------------------------------------------------------------- | ------------------------------------------------------------------------| --------------------------------------------------|
| Timeseries         | `model.sandbox_ops.timeseries_ops.createOne                   ` | create one timeseries in sandbox                                        | [model_workflow.py](examples/model_workflow.py)   |
|                    | `model.sandbox_ops.timeseries_ops.create                      ` | create multiple timeseries in sandbox                                   |                                                   |
|                    | `model.sandbox_ops.timeseries_ops.update                      ` | update a sandbox timeseries                                             |                                                   |
|                    | `model.sandbox_ops.timeseries_ops.deploy                      ` | deploy a sandbox timeseries in production                               | [model_workflow.py](examples/model_workflow.py)   |
|                    |                                                                 |                                                                         | [model_workflow.py](examples/model_workflow.py)   |
| Object Attributes  | `model.sandbox_ops.object_attributes_ops_ops.createOne        ` | create one object attribute in sandbox                                  |                                                   |
|                    | `model.sandbox_ops.object_attributes_ops_ops.create           ` | create multiple object attributes in sandbox                            |                                                   |
|                    | `model.sandbox_ops.object_attributes_ops_ops.update           ` | update a sandbox object attribute                                       |                                                   |
|                    | `model.sandbox_ops.object_attributes_ops_ops.deploy           ` | deploy a sandbox object attribute in production                         | [model_workflow.py](examples/model_workflow.py)   |
|                    |                                                                 |                                                                         | [model_workflow.py](examples/model_workflow.py)   |
| Owner Attributes   | `model.sandbox_ops.owner_attributes_ops.createOne             ` | create one owner attribute in sandbox                                   |                                                   |
|                    | `model.sandbox_ops.owner_attributes_ops.create                ` | create multiple owner attributes in sandbox                             |                                                   |
|                    | `model.sandbox_ops.owner_attributes_ops.update                ` | update a sandbox owner attribute                                        |                                                   |
|                    | `model.sandbox_ops.owner_attributes_ops.deploy                ` | deploy a sandbox owner attribute in production                          | [model_workflow.py](examples/model_workflow.py)   |
|                    |                                                                 |                                                                         |                                                   |
| Event Types        | `model.sandbox_ops.event_types_ops.createOne                  ` | create one event type                                                   | [model_workflow.py](examples/model_workflow.py)   |
|                    | `model.sandbox_ops.event_types_ops.create                     ` | create multiple event types                                             |                                                   |
|                    | `model.sandbox_ops.event_types_ops.update                     ` | update a event type                                                     |                                                   |
|                    | `model.sandbox_ops.event_types_ops.delete                     ` | delete a sandbox event type                                             |                                                   |
|                    | `model.sandbox_ops.event_types_ops.add_relation               ` | add a relation to a timeseries                                          |                                                   |
|                    | `model.sandbox_ops.event_types_ops.remove_relation            ` | delete a relation to a timeseries                                       |                                                   |
|                    |                                                                 |                                                                         |                                                   |
| Object Types       | `model.sandbox_ops.object_types_ops.createOne                 ` | create one object type                                                  | [model_workflow.py](examples/model_workflow.py)   |
|                    | `model.sandbox_ops.object_types_ops.create                    ` | create multiple object types                                            |                                                   |
|                    | `model.sandbox_ops.object_types_ops.update                    ` | update a object type                                                    |                                                   |
|                    | `model.sandbox_ops.object_types_ops.delete                    ` | delete a sandbox object type                                            |                                                   |
|                    | `model.sandbox_ops.object_types_ops.add_relation              ` | add a relation to an object attribute                                   |                                                   |
|                    | `model.sandbox_ops.object_types_ops.remove_relation           ` | delete a relation to an object attribute                                |                                                   |


---
# 3. Requirements

- Python 3.6, 3.7, 3.8 or 3.9
- libraries: `requests`, `tenacity` (for exponential backoff)


---
# 4. Installation & Configuration

From [PyPI](https://pypi.python.org/pypi/smartobjects/):

    $ pip install smartobjects

Alternatively, if you want to use the client from a data science perspective you can install with `pandas` extra (see [Search Services](###use-the-search-services):

    $ pip install smartobjects[pandas]

From the sources:

    $ git clone https://github.com/mnubo/smartobjects-python-client.git
    $ cd smartobjects-python-client
    $ python setup.py install

---
# 5. Usage

### Initialize the MnuboClient

```python
from smartobjects import SmartObjectsClient
from smartobjects import Environments, ExponentialBackoffConfig

client = SmartObjectsClient('<CLIENT_ID>', '<CLIENT_SECRET>', Environments.Production)
client_with_backoff = SmartObjectsClient('<CLIENT_ID>', '<CLIENT_SECRET>', Environments.Production, backoff_config=ExponentialBackoffConfig())
```

The environment argument can be `Environments.Sandbox` or `Environments.Production` or one of your custom urls to access the mnubo platform.

You can generate an App Token from the web application and use it with this SDK.

Note: App Tokens can have restricted access to specific APIs and can be disabled by an administrator at any given time. This means that some API provided in this SDK may not work correctly.

```python
from smartobjects import SmartObjectsClient
from smartobjects import Environments, ExponentialBackoffConfig

client = SmartObjectsClient.withToken('<YOUR_TOKEN>', Environments.Sandbox)
client_with_backoff = SmartObjectsClient.withToken('<YOUR_TOKEN>', Environments.Sandbox, backoff_config=ExponentialBackoffConfig())
```

_Optional arguments_:

- compression_enabled: if `True`, data sent to the platform is compressed using _gzip_ format. Default: `True`
- backoff_config: if given, requests resulting in 503 will be retried. Default: `None`
- token_override: if given, the OAuth2 dance is avoid and this token is always used. Default: `None`

_Note:_ to use exponential backoff retries feature, you must `pip install tenacity` (4.2.0+)

### Use the Owners service
To create owners on the mnubo SmartObjects platform, please refer to
the data modeling guide to format correctly the owner's data structure.

#### Create an Owner
```python
client.owners.create({
    "username": "sheldon.cooper@caltech.edu",
    "x_password": "****************",
    "zip_code": "91125"
})
```

_Mandatory properties_: `username`, `x_password`

#### Claim or unclaim a Smart Object for an Owner
```python
client.owners.claim('sheldon.cooper@caltech.edu', 'fermat1901')
# if you want to override some values
client.owners.claim('sheldon.cooper@caltech.edu', 'fermat1901', {
    "x_timestamp": "2015-02-01T05:00:00.000Z"
})


client.owners.unclaim('sheldon.cooper@caltech.edu', 'fermat1901')
# if you want to override some values
client.owners.unclaim('sheldon.cooper@caltech.edu', 'fermat1901', {
    "x_timestamp": "2015-02-01T05:00:00.000Z"
})
```

As a batch:
```python
client.owners.batch_claim([
    ('sheldon.cooper@caltech.edu', 'fermat1901'),
    ('leonard.hofstadter@caltech.edu', 'ramanujan1887')
])
```

#### Update an Owner
```python
client.owners.update('sheldon.cooper@caltech.edu', {
    "zip_code": "94305",    # update of an existing property
    "service_type": "phd"   # creation of a new property
})
```
#### Create or update owners in batch
```python
results = client.owners.create_update([
    {"username": "sheldon.cooper@caltech.edu", "service_type": "prof"},
    {"username": "leonard.hofstadter@caltech.edu", "x_password": "*******"}
])
```
_Mandatory properties_: `x_username_id` (all owners), `x_x_password_type` (new owners)

Returns a list of `Result` with the completion status of each operation (and reason of failure if any).

#### Delete an Owner
```python
client.owners.delete('sheldon.cooper@caltech.edu')
```

#### Check if an owner exists

```python
>>> client.owners.owner_exists('sheldon.cooper@caltech.edu')
True

>>> client.owners.owners_exist(['sheldon.cooper@caltech.edu', 'hwolowitz.phd@caltech.edu'])
{'sheldon.cooper@caltech.edu': True, 'hwolowitz.phd@caltech.edu': False}
```


### Use the Smart Objects Service
To create smart objects on the mnubo SmartObjects platform, please refer to
the data modeling guide to format correctly the smart object's data structure.

#### Create a Smart Object
```python
client.objects.create({
    "x_device_id": "fermat1901",
    "x_object_type": "calculator",
    "precision": "infinite"
})
```
_Mandatory properties_: `x_device_id`, `x_object_type`

#### Update a Smart Object
```python
client.objects.update("fermat1901", {
    "is_valid": True
})
```

#### Create or update objects in batch

If an object doesn't exist, it will be created, otherwise it will be updated.

```python
client.objects.create_update([
    {"x_device_id": "fermat1901", "is_valid": False},
    {"x_device_id": "ramanujan1887", "x_object_type": "pie"}
])
```
_Mandatory properties_: `x_device_id` (all objects), `x_object_type` (new objects)

Returns a list of `Result` objects with the completion status of each operation (and reason of failure if any).

#### Delete a Smart Object
```python
client.objects.delete("fermat1901")
```

#### Check if an object exists

```python
>>> client.objects.object_exists('fermat1901')
True

>>> client.objects.objects_exist(['fermat1901', 'teleporter'])
{'fermat1901': True, 'teleporter': False}
```


### Use the Event Services
To send events to the mnubo SmartObjects platform, please refer to
the data modeling guide to format correctly the event's data structure.

#### Send an Event
```python
results = client.events.send([
    {"x_object": {"x_device_id": "fermat1901"}, "status": "running"},
    {"x_object": {"x_device_id": "ramanujan1887"}, "ratio": 3.1415}
])
```

_Optional arguments_:
- `must_exist`: if `True`, an event referring an unknown object will be rejected (default to `False`)
- `report_results`: if `True`, a list of `EventResult` objects will be returned with the status of each operation.
      If `False`, nothing will be returned when _all_ events are successfully ingested, but a `ValueError` exception
      will be thrown if at least one fail. Default to `True`.

#### Send an event tagged with a device

This method allows sending multiple events for a given device without the need of setting the target in the payload.

```python
results = client.events.send_from_device("ramanujan1887", [
    {"ratio": 3.1414},
    {"ratio": 3.1413}
])
```

_Optional arguments_:
-   `report_results`: if `True`, a list of `EventResult` objects will be returned with the status of each operation.
    If `False`, nothing will be returned when _all_ events are successfully ingested, but a `ValueError` exception
    will be thrown if at least one fail. Default to `True`.


#### Check if an event already exists

```python
>>> client.events.event_exists(UUID("1ff58794-f0da-4738-8444-68a592de6746"))
True

>>> client.events.events_exist([UUID("1ff58794-f0da-4738-8444-68a592de6746"), uuid.uuid4()])
{UUID("1ff58794-f0da-4738-8444-68a592de6746"): True, UUID("e399afda-3c8b-4a6d-bf9c-c51b846c214d"): False}
```


### Use the Search Services
To send search queries to the mnubo SmartObjects platform, please refer to
the Search API documentation to format your queries correctly.

#### Search Query
```python
resultset = client.search.search({
    "from": "owner",
    "limit": 100,
    "select": [
        {"value": "username"}
    ]
})
```

This method returns a `ResultSet` containing the result of the search (columns and rows).

```python
>>> "Got {} results!".format(len(resultset))
Got 2 results!
>>> [row.get("username") for row in resultset]
["sheldon.cooper@caltech.edu", "leonard.hofstadter@caltech.edu"]
```

Optionally, if you are using the SDK with [pandas](http://pandas.pydata.org/pandas-docs/stable/index.html), you can use the propery `df` of the `resultset`. It will return a DataFrame version of the results, with `datetime` columns converted to a [datetime](http://pandas.pydata.org/pandas-docs/stable/generated/pandas.to_datetime.html#pandas.to_datetime) structure.

```python
resultset = client.search.search({
    "from": "event",
    "select": [
        {"count": "*"}
    ],
    "groupByTime": {
        "interval": "year",
        "field": "x_timestamp"
    }
})

resultset.df
#                   year  COUNT(*)
# 0 2017-01-01 05:00:00      1232
```

#### Validate a search query

For complex queries, it is recommended to use this feature to reduce errors.

```python
validation_result = client.search.validate_query({
    "invalid": "owner",
    "limit": 100,
    "select": [
        {"value": "username"}
    ]
})
```

This method returns a `QueryValidationResult` object with the status of the validation and list of errors if any:

```python
>>> validation_result.is_valid
False
>>> validation_result.validation_errors
["a query must have a 'from' field"]
```


#### Retrieve namespace datasets

This method allows to retrieve the different datasets available for querying. Result is a map of `DataSet` objects
indexed by the dataset name (`owner`, `object`, `event`, `session`).

```python
>>> datasets = client.search.get_datasets()
>>> [event.key for event in datasets['event'].fields]
["event_id", "x_object.x_device_id", "timestamp", ...]
```

### Use the Model Service

#### Retrieve the model

To retrieve the model as it is currently in the zone you are working (sandbox or production), you can use
the ModelService:

```python
model = client.model.export()
print(len(model.eventTypes)) # outputs: 2
```

#### Get Timeseries

```python
tss = client.model.get_timeseries()
print("Number of Timeseries: {}", len(tss))
```
#### Get Object Attributes

```python
objs = client.model.get_object_attributes()
print("Number of Object Attributes: {}", len(objs))
```
#### Get Owner Attributes

```python
owners = client.model.get_owner_attributes()
print("Number of Owner Attributes: {}", len(owners))
```
#### Get Event Types

```python
ets = client.model.get_event_types()
print("Number of Event Types: {}", len(ets))
```
#### Get Object Types

```python
ots = client.model.get_object_types()
print("Number of Object Types: {}", len(ots))
```


#### Sandbox only operations

##### Create multiple event types

```python
client.model.sandbox_ops.event_types_ops.create([{
    'key': 'key',
    'origin': 'scheduled',
    'description': '',
    'timeseriesKeys': []
}])
```

##### Create one event type

```python
client.model.sandbox_ops.event_types_ops.createOne({
    'key': 'key',
    'origin': 'scheduled',
    'description': '',
    'timeseriesKeys': []
})
```

##### Update an event type

```python
client.model.sandbox_ops.event_types_ops.update(key, {
    'key': 'key',
    'origin': 'unscheduled',
    'description': 'new description',
    'timeseriesKeys': []
})
```

##### Delete an event type

```python
client.model.sandbox_ops.event_types_ops.delete(key)
```




##### Create multiple object types

```python
client.model.sandbox_ops.object_types_ops.create([{
    'key': 'key',
    'description': '',
    'objectAttributesKeys': []
}])
```


##### Create one object type

```python
client.model.sandbox_ops.object_types_ops.createOne({
    'key': 'key',
    'description': '',
    'objectAttributesKeys': []
})
```


##### Update an object type

```python
client.model.sandbox_ops.object_types_ops.update(key, {
    'key': 'key',
    'description': 'new description',
    'timeseriesKeys': []
})
```


##### Delete an object type

```python
client.model.sandbox_ops.object_types_ops.delete(key)
```



##### Create multiple timeseries

```python
client.model.sandbox_ops.timeseries_ops.create([{
    'key': 'ts_key',
    'displayName': '',
    'description': '',
    'type': {
        'highLevelType': 'TEXT'
    },
    'eventTypeKeys': [key]
}])
```


##### Create one timeseries

```python
client.model.sandbox_ops.timeseries_ops.createOne({
    'key': 'ts_key',
    'displayName': '',
    'description': '',
    'type': {
        'highLevelType': 'TEXT'
    },
    'eventTypeKeys': [key]
})
```


##### Update a timeseries

```python
client.model.sandbox_ops.timeseries_ops.update(
    'ts_key',
    {
        'displayName': 'new desc',
        'description': 'new dp',
    }
)
```


##### Deploy a timeseries in production

```python
client.model.sandbox_ops.timeseries_ops.deploy('ts_key')
```


##### Create multiple object attributes

```python
client.model.sandbox_ops.object_attributes_ops.create([{
    'key': 'obj_key',
    'displayName': '',
    'description': '',
    'type': {
        'containerType': 'none',
        'highLevelType': 'AREA'
    },
    'objectTypeKeys': [key]
}])
```


##### Create one object attribute

```python
client.model.sandbox_ops.object_attributes_ops.createOne({
    'key': 'obj_key',
    'displayName': '',
    'description': '',
    'type': {
        'containerType': 'none',
        'highLevelType': 'AREA'
    },
    'objectTypeKeys': [key]
})
```


##### Update one object attribute

```python
client.model.sandbox_ops.object_attributes_ops.update(
    'obj_key',
    {
        'displayName': 'new desc',
        'description': 'new dp',
    }
)
```

##### Deploy an object attribute in production

```python
client.model.sandbox_ops.object_attributes_ops.deploy('obj_key')
```


##### Create multiple owner attributes

```python
client.model.sandbox_ops.owner_attributes_ops.create([OwnerAttribute({
    'key': 'owner_key',
    'displayName': '',
    'description': '',
    'type': {
        'containerType': 'none',
        'highLevelType': 'FLOAT'
    }
})])
```


##### Create one owner attribute

```python
client.model.sandbox_ops.owner_attributes_ops.createOne(OwnerAttribute({
    'key': 'owner_key',
    'displayName': '',
    'description': '',
    'type': {
        'containerType': 'none',
        'highLevelType': 'FLOAT'
    }
}))
```


##### Update one owner attribute

```python
client.model.sandbox_ops.owner_attributes_ops.update(
    'owner_key',
    {
        'displayName': 'new desc',
        'description': 'new dp',
    }
)
```

##### Deploy an owner attribute in production

```python
client.model.sandbox_ops.owner_attributes_ops.deploy('owner_key')
```


### Use the Datalake Service

#### Create a Dataset

```python
from smartobjects.datalake.datasets import Dataset, DatasetField

dataset_field = DatasetField(key="my_field", type="BOOLEAN")
dataset = Dataset(key="my_dataset", fields=[dataset_field])
client.datalake.create(dataset)
```

#### Delete a Dataset

```python
client.datalake.delete("my_dataset")
```

#### List Datasets
```python
list_of_datasets = client.datalake.list()
```

#### Update a Dataset
```python
from smartobjects.datalake.datasets import DatasetUpdate

update_dataset = DatasetUpdate(displayName="myupdatedschema", description="my updated schema",
                              metadata={"additionalProp4": "updated_metadata"})

client.datalake.update(datasetKey="my_dataset", dataset=update_dataset)
```

#### Get a dataset definition
```python
dataset_definition = client.datalake.get("my_dataset")
```

#### Add a Dataset field
```python
from smartobjects.datalake.datasets import DatasetField

new_field = DatasetField(key="new_field", type="BOOLEAN")
client.datalake.add_field(datasetKey="my_dataset", datasetField=new_field)
```

#### Update a Dataset field
```python
from smartobjects.datalake.datasets import DatasetFieldUpdate

field_update = DatasetFieldUpdate(description="updated_string", displayName="updated_string")
client.datalake.update_field(datasetKey="my_dataset", fieldKey="my_new_field", datasetField=field_update)
```

#### Send data to a Dataset
```python
data = [{"my_field": True}, {"my_other_field": 42}]
client.datalake.send(datasetKey="my_dataset", data=data)
```


# 6. Need help?

Reach us at support@mnubo.com
