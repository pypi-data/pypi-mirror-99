# Apache Airflow Provider for Fivetran

Provides an Airflow operator, sensor, and hook for [Fivetran](https://fivetran.com). This allows you to start Fivetran jobs from Airflow, and monitor a Fivetran sync job for completion before running downstream processes.

Fivetran automates your data pipeline, and Airflow automates your data processing.

## Installation

Pre-requisites: An environment running `apache-airflow`.

```
pip install airflow-provider-fivetran
```

## Configuration

In the Airflow user interface, you will need to configure a Connection for Fivetran. Most of the Connection config fields will be left blank. Configure the following fields:

* `Conn Id`: `fivetran`
* `Conn Type`: `HTTP`
* `Login`: Fivetran API Key
* `Password`: Fivetran API Secret

Fivetran API Key and Secret can be found in the [Fivetran Account Settings](https://fivetran.com/account/settings), under the **API Config** section. Please see our documentation for more information on [Fivetran API Authentication](https://fivetran.com/docs/rest-api/getting-started#authentication).

The sensor and operator assume the `Conn Id` is set to `fivetran`, however if you are managing multipe Fivetran accounts, you can set this to anything you like. See the DAG in examples to see how to specify a custom `Conn Id`.

## Modules

### [Fivetran Operator](./fivetran_provider/operators/fivetran.py)

Starts a Fivetran sync job. Note that when a Fivetran sync job is controlled via an Operator, it is no longer run on the schedule as managed by Fivetran. In other words, it is now scheduled only from Airflow.

`FivetranOperator` requires that you specify the `connector_id` of the sync job to start. You can find `connector_id` in the Settings page of the connector you configured in the [Fivetran interface](https://fivetran.com/dashboard/connectors).

Import into your DAG via:
```
from fivetran_provider.operators.fivetran import FivetranOperator
```

### [Fivetran Sensor](./fivetran_provider/sensors/fivetran.py)

Monitors a Fivetran sync job for completion. This allows you to trigger downstream processes only when one or more Fivetran sync jobs have completed, ensuring data consistency.

Note, it is possible to monitor a sync that is scheduled and manaaged from Fivetran; in other words, you can use `FivetranSensor` without using `FivetranOperator`. If used in this way, your DAG will wait until the sync job starts on its Fivetran-controlled schedule and then completes.

`FivetranSensor` requires that you specify the `connector_id` of the sync job to start. You can find `connector_id` in the Settings page of the connector you configured in the [Fivetran interface](https://fivetran.com/dashboard/connectors).

Import into your DAG via:
```
from fivetran_provider.sensors.fivetran import FivetranSensor
```

## Examples

See the [**examples**](./fivetran_provider/examples) directory for an example DAG.

## Issues

Please submit [issues](https://github.com/fivetran/airflow-provider-fivetran/issues) and [pull requests](https://github.com/fivetran/airflow-provider-fivetran/pulls) in our official repo:
[https://github.com/fivetran/airflow-provider-fivetran](https://github.com/fivetran/airflow-provider-fivetran)

We are happy to hear from you, for any feedback please email the authors at [devrel@fivetran.com](mailto:devrel@fivetran.com).


## Acknowledgements

Special thanks to [Pete DeJoy](https://github.com/petedejoy), [Plinio Guzman](https://github.com/pgzmnk), and [David Koenitzer](https://github.com/sunkickr) of [Astronomer.io](https://www.astronomer.io/) for their contributions and support in getting this provider off the ground.

