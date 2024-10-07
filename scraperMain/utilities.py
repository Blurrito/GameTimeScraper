import os
from datetime import datetime, timedelta

def toTimestamp(self, value):
    # Validate category has a recorded time
    if value == '--':
        return datetime(0,0,0).time()

    # Determine if it's an exact time or an estimate
    rangeValues = []
    if '-' in value:
        rangeValues = value.split('-')
    if len(rangeValues) == 0:
        rangeValues.append(value)

    processedValues = []
    for rangeValue in rangeValues:
        # Transform all estimates to the same format
        # Example: 65½ Hours -> 65h 30m
        strippedValue = rangeValue
        if '½' in value:
            strippedValue = strippedValue.replace('½', '') + ' 30m'
        if 'Hours' in value:
            strippedValue = strippedValue.replace(' Hours', 'h')
        splitValue = strippedValue.split(' ')

        # Transform the generalized time to a colon-separated timestamp
        # Example: 65h 30m -> 65:30:00
        timestampValues = ['0', '0', '0']
        for value in splitValue:
            unit = value[-1]
            if unit == 'h':
                timestampValues[0] = value[:-1]
            if unit == 'm':
                timestampValues[1] = value[:-1]
            if unit == 's':
                timestampValues[2] = value[:-1]

        processedValues.append(f"{timestampValues[0]}:{timestampValues[1]}:{timestampValues[2]}")

    # Return timestamp as a range if more than one is present
    # Example: 65:30:00-87:45:00
    if len(processedValues) > 1:
        return f"{processedValues[0]}-{processedValues[1]}"
    return processedValues[0]

def toNumber(self, value):
    strippedValue = value
    if '.' in value:
        strippedValue = strippedValue.replace('.', '')
        if 'K' in value:
            strippedValue = strippedValue[:-1] + '00'

    if 'K' in strippedValue:
        strippedValue = strippedValue[:-1] + '000'
    if '%' in strippedValue:
        strippedValue = strippedValue[:-1]
    return int(strippedValue)