**This file is part of pvoutput-publisher**

# License
pvoutput-publisher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

pvoutput-publisher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pvoutput-publisher.  If not, see <https://www.gnu.org/licenses/>.    

# pvoutput-publisher
pvoutput-publisher is independent from the type of inverter you have so can be used with any inverter library that you have to publish to pvoutput.org.
The main reason for this library is to shield the user from the intricacies of generating or parsing fixed position data.

## Add Status
To publish a single reading to pvoutput.org is taking a single AddStatus object and filling as many fields as you have available.
So assuming you have added your imports (see further down) and you have a status object, the publish is a single line and if no error was raised, you know it was successful:

    response = publish_data(ADD_STATUS_SERVICE_NAME, status, SystemDetails(api_key="api1", system_id="sysid1"), ADD_STATUS_URL)
 

One or more of the following 4 fields must be present as per the [Add Status][] Notes:

    power_generation=2001,
    power_consumption=2101,
    energy_consumption=10001,
    energy_generation=11001,

### Donation Mode
If you make donations to pvoutput.org you can specify the donation mode fields:  

    extended_value_1=11.1,
    extended_value_2=12.1,
    extended_value_3=1,
    extended_value_4=14.1,
    extended_value_5=15.1,
    extended_value_6=16.1,
    text_message_1="Hi Ho"

### Date/Times
Date and time are from the [datetime library](https://docs.python.org/3/library/datetime.html#module-datetime) - datetime.**date** and datetime.**time** objects

### For current date and time:
    
    current_date_time = datetime.now()
    current_date = current_date_time.date()  
    current_time = current_date_time.time()
    
### For a date and time in the past:

    date = date(2020, 10, 26)
    time = time(18, 30)

### Cumulative Flag    
In my system, my energy generation figures is a lifetime value that always increases and doesn't reset in the inverter at the start of the day.
So my cumulative_flag is 1 (or 2 since I don't measure consumption). pvoutput works out the generation at any given time during the day by subtracting the first value of the day.     

### Constants

To call the publish_data method, you need to pass some values that are the same every time you call the method.
You can import these values such as the service name, which is used to pick the correct processing code
and the url of the pvoutput.org service/api that gets called.

## Full example:   
Note the order of the parameters is not important. The publish_data will assign the values to the appropriate parameter in the Add Status service call.
The list of parameters shown here matches up with the names and positions in the    
    
    from pvoutput_api.constants import ADD_STATUS_SERVICE_NAME, ADD_STATUS_URL, ADD_BATCH_STATUS_URL, ADD_BATCH_STATUS_SERVICE_NAME
    from pvoutput_api.publisher import publish_data
    
    status = AddStatus(date(2020, 10, 26),
                           time(15, 30),
                           energy_generation=11001,
                           power_generation=2001,
                           energy_consumption=10001,
                           power_consumption=2101,
                           temperature=22.1,
                           voltage=233.1,
                           cumulative_flag=1,
                           net_flag=0,
                           extended_value_1=11.1,
                           extended_value_2=12.1,
                           extended_value_3=1,
                           extended_value_4=14.1,
                           extended_value_5=15.1,
                           extended_value_6=16.1,
                           text_message_1="Hi Ho"
                           )

    response = publish_data(ADD_STATUS_SERVICE_NAME, status, SystemDetails(api_key="api1", system_id="sysid1"), ADD_STATUS_URL)
    # Published ok code=200
    print("Published ok code={}".format(response.resp.status_code))

## Adding some error handling

Can't have reading date too far back in past, see [API errors]:

    status = AddStatus(date(2020, 1, 26),... text_message_1="Hi Ho")

    try:
        response = publish_data(ADD_STATUS_SERVICE_NAME, status, system, ADD_STATUS_URL)
    except HTTPError as e:
        # Error publishing: b'Bad request 400: Date is older than 14 days [20200126]'
        print("Error publishing: {}".format(e.response.content))
        raise # pass on error

[Add Status]: https://pvoutput.org/help.html#api-addstatus
[API errors]: https://pvoutput.org/help.html#api-errors 

## Add Batch Status
This is similar in usage to [Add Status](#Add Status) and would typically use this if you for example lost wifi connectivity and wanted to catch up.

    status1 = AddStatus(date(2020, 1, 26), time(15, 30),... extended_value_6=11.5)
    status2 = AddStatus(date(2020, 1, 26), time(15, 35),... extended_value_6=11.6)
    batch_statuses = AddBatchStatus()
    statuses.add_status(status1)
    statuses.add_status(status2)
    
    try:
        response = publish_data(ADD_BATCH_STATUS_SERVICE_NAME, batch_statuses, system, ADD_BATCH_STATUS_URL)
    except HTTPError as e:
        # Error publishing: b'Bad request 400: Date is older than 14 days [20200126]'
        print("Error publishing: {}".format(e.response.content))
        raise # pass on error

### Handling successful batch publish, but some entries did not cause an update

In batch mode, not all entries will cause an update. This is likely ok, but could indicate some issues with your data points.
But instead of having to parse the fixed length/position replies you can get easy access:

    try:
        response = publish_data(ADD_BATCH_STATUS_SERVICE_NAME, batch_statuses, system, ADD_BATCH_STATUS_URL)
    except HTTPError as e:
        # if some batch entries do not cause any data updates, this is not a failure.
        raise 
     
    for reading_response in response.statuses:
    if reading_response.status_added:
        print("Reading {} {} was added".format(reading_response.date, reading_response.time))
    else:
        print("Reading {} {} did not add or update any data".format(reading_response.date, reading_response.time))
    
So for a response of two readings where the first was added (status1 from above) and the second was not (status2 from above), it would print out something like:

    Reading 2020-01-26 15:30:00 was added
    Reading 2020-01-26 15:35:00 did not add or update any data 
