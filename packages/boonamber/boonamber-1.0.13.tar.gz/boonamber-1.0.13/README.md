# Boon Amber Python SDK

An SDK for Boon Amber sensor analytics

- __Website__: [boonlogic.com](https://boonlogic.com)
- __Documentation__: [Boon Docs Main Page](https://docs.boonlogic.com)
- __SDK Functional Breakdown__: [amber-python-sdk classes and methods](https://boonlogic.github.io/amber-python-sdk/docs/boonamber/index.html)

## Installation

The Boon Amber SDK is a Python 3 project and can be installed via pip.

```
pip install boonamber
```

## Credentials setup

Note: An account in the Boon Amber cloud must be obtained from Boon Logic to use the Amber SDK.

The username and password should be placed in a file named _~/.Amber.license_ whose contents are the following:

```json
{
    "default": {
        "username": "AMBER-ACCOUNT-USERNAME",
        "password": "AMBER-ACCOUNT-PASSWORD",
        "server": "https://amber.boonlogic.com/v1"
    }
}
```

The _~/.Amber.license_ file will be consulted by the Amber SDK to find and authenticate your account credentials with the Amber server. Credentials may optionally be provided instead via the environment variables `AMBER_USERNAME` and `AMBER_PASSWORD`.

## Connectivity test

The following Python script provides a basic proof-of-connectivity:

[connect-example.py](examples/connect-example.py)

```python
from boonamber import AmberClient

# At initialization the client discovers Amber account credentials
# under the "default" entry in the ~/.Amber.license file.
amber = AmberClient()

sensors = amber.list_sensors()
print("sensors: {}".format(sensors))
```

Running the connect-example.py script should yield output like the following:
```
$ python connect-example.py
sensors: {}
```
where the dictionary `{}` lists all sensors that currently exist under the given Boon Amber account.

## Full Example

The following Python script will demonstrate each API call in the Amber Python SDK.

[full-example.py](examples/full-example.py)

```python
import sys
from boonamber import AmberClient, AmberCloudError, AmberUserError

"""Demonstrates usage of all Amber SDK endpoints."""

# connect with default license
# use 'license_id=<name>' to specify something other than 'default'
amber = AmberClient()

# List all sensors belonging to current user
print("listing sensors")
try:
    sensors = amber.list_sensors()
except AmberCloudError as e:
    print(e)
    sys.exit(1)
except AmberUserError as e:
    print(e)
    sys.exit(1)
print("sensors: {}".format(sensors))
print()

# Create a new sensor
print("creating sensor")
try:
    sensor_id = amber.create_sensor('new-test-sensor')
except AmberCloudError as e:
    print(e)
    sys.exit(1)
except AmberUserError as e:
    print(e)
    sys.exit(1)
print("sensor-id: {}".format(sensor_id))
print()

# Get sensor info
print("getting sensor")
try:
    sensor = amber.get_sensor(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("sensor: {}".format(sensor))
print()

# Update the label of a sensor
print("updating label")
try:
    label = amber.update_label(sensor_id, 'test-sensor')
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("label: {}".format(label))
print()

# Configure a sensor
print("configuring sensor")
try:
    config = amber.configure_sensor(sensor_id, feature_count=1, streaming_window_size=25)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("config: {}".format(config))
print()

# Get sensor configuration
print("getting configuration")
try:
    config = amber.get_config(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("config: {}".format(config))
print()

# Stream data to a sensor
print("streaming data")
data = [0, 1, 2, 3, 4]
try:
    results = amber.stream_sensor(sensor_id, data)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("results: {},".format(results))
print()

# Get clustering status from a sensor
print("getting status")
try:
    status = amber.get_status(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("status: {}".format(status))
print()

# Delete a sensor instance
print("deleting sensor")
try:
    amber.delete_sensor(sensor_id)
except AmberCloudError as e:
    print("Amber Cloud error: {}".format(e))
    sys.exit(1)
except AmberUserError as e:
    print("Amber user error: {}".format(e))
    sys.exit(1)
print("succeeded")
print()
```


## Advanced CSV file processor

The following will process a CSV file using batch-style streaming requests.  Full Amber analytic results will be displayed after each streaming request.  

[stream-advanced.py](examples/stream-advanced.py)<br>
[output_current.csv](examples/output_current.csv)

```python
import csv
import sys
from datetime import datetime
from boonamber import AmberClient, AmberCloudError

"""Demonstrates a streaming use case in which we read continuously
   from a CSV file, inference the data line by line, and print results.
"""


class AmberStream:

    def __init__(self, sensor_id=None):
        """
        Initializes the AmberStream example class.
        :param sensor_id: The sensor_id to be used by AmberStream.  If sensor_id is None, then a sensor is created
        """
        self.data = []
        self.sample_cnt = 0

        try:
            self.amber = AmberClient()
            if sensor_id is None:
                self.sensor_id = self.amber.create_sensor(label='stream-example-sensor')
                print("created sensor {}".format(sensor_id))
            else:
                self.sensor_id = sensor_id
                print("using sensor {}".format(sensor_id))

            config = self.amber.configure_sensor(sensor_id, feature_count=1, streaming_window_size=25,
                                                 samples_to_buffer=1000, learning_max_clusters=1000,
                                                 learning_max_samples=20000, learning_rate_numerator=0,
                                                 learning_rate_denominator=20000)
            print("{} config: {}".format(self.sensor_id, config))
        except AmberCloudError as e:
            print(e)
            sys.exit(1)

    def do_analytics(self):
        """
        Run analytics based on self.data and provide example of formatted results
        :return: None
        """
        self.sample_cnt += len(self.data)
        d1 = datetime.now()
        results = self.amber.stream_sensor(self.sensor_id, self.data)
        d2 = datetime.now()
        delta = (d2 - d1).microseconds / 1000
        print("State: {}({}%), inferences: {}, clusters: {}, samples: {}, duration: {}".format(
            results['state'], results['progress'], results['totalInferences'], results['clusterCount'], self.sample_cnt,
            delta))
        for analytic in ['ID', 'SI', 'AD', 'AH', 'AM', 'AW']:
            if analytic == 'AM':
                analytic_pretty = ','.join("{:.6f}".format(a) for a in results[analytic])
            else:
                analytic_pretty = ','.join("{}".format(a) for a in results[analytic])
            print("{}: {} ".format(analytic, analytic_pretty))
        self.data = []

    def stream_csv(self, csv_file, batch_size=20):
        """
        Given a path to a csv file, stream data to Amber in sizes specified by batch_size
        :param csv_file: Path to csv file
        :param batch_size: Batch size to be used on each request
        :return: None
        """
        # Open csv data file and begin streaming
        with open(csv_file, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.data = []
            self.sample_cnt = 0
            for row in csv_reader:
                for d in row:
                    self.data.append(float(d))
                    if len(self.data) == batch_size:
                        try:
                            self.do_analytics()
                        except Exception as e:
                            print(e)
                            sys.exit(1)

            # send the remaining partial batch (if any)
            if len(self.data) > 0:
                self.do_analytics()


streamer = AmberStream(sensor_id='b76b3cc542f434a7')
streamer.stream_csv('output_current.csv', batch_size=25)
```

### Sample output:

```
State: Monitoring(0%), inferences: 20201, clusters: 247, samples: 20275, duration: 228.852
ID: 29,30,31,32,33,34,35,36,37,38,39,245,41,42,219,44,45,220,47,48,49,50,51,52,1 
SI: 306,307,307,307,307,307,307,308,308,308,308,308,309,311,315,322,336,364,421,532,350,393,478,345,382 
AD: 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 
AH: 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 
AM: 0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013,0.000013 
AW: 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 
```
