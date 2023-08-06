sumoq
===============
sumoq is a tiny command-line utility to query sumologic.

### Installing
===============
```
pip install sumoq
```

### Config file
===============
To run this utiliity, a config file(~/.sumo) is required to be created, here is an exmaple:
```
[default]
sumo_access_key_id = <GET_IT_FROM_SUMOLOGIC_WEBSITE>
sumo_secret_access_key = <GET_IT_FROM_SUMOLOGIC_WEBSITE>
timezone = PST
```

### Usage
===============

```
[fei.ni@fei-ni-C02D72XMMD6N-SM  dist (main *%)]$ sumoq -h
Usage: [-] Usage echo 'query_string' | sumoq [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -r RECENT_HOURS, --recent_hours=RECENT_HOURS
                        time range to query till now, default is 6 which means
                        recent 6 hours (optional)
  -s START_TIME, --start_time=START_TIME
                        start time to query, format is YYYY-MM-DDTH:M:S, such
                        as 2021-01-01T00:00:00 (optional)
  -e END_TIME, --end_time=END_TIME
                        end time to query, format is YYYY-MM-DDTH:M:S, such as
                        2021-01-01T00:00:00 (optional)
  -l LIMIT, --limit=LIMIT
                        limited items' number to return (optional)
```

If no options spcified, the default behavior is to run query in recent 6 hours.

### Examples
===============

```
# To query string "393365073" in those logs collected in recent 6 hours, in this case, 393365073 is the requestid
echo "393365073" |sumoq >393365073.log

# To query string "393365073" in those logs collected in recent 24 hours
echo "393365073" |sumoq -r 24 >393365073.log

# To query string "393365073" in those logs collected between 2021-01-01T00:00:00 and 2021-01-02T00:00:00
echo "393365073" |sumoq -s 2021-01-01T00:00:00 -t 2021-01-02T00:00:00 24 >393365073.log

# To query  service-production's log parsed by json and sorted timestamp asc in recent 6 hours
echo '_sourceHost="service-production" | json auto |sort timestamp asc' | sumoq >service.log
```
