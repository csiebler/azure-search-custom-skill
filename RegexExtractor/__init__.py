import logging
import azure.functions as func
import json
import re

regex = r'(P\d{6,10})'

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse("Invalid body", status_code=400)
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse("Invalid body", status_code=400)


def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {
        "values": []
    }

    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)

## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError as error:
        return None

    # Validate the inputs, those also define the names for the skill
    try:         
        assert ('data' in value), "'data' field is required."
        data = value['data']
        assert ('text' in data), "'text' field is required in 'data' object."
    except AssertionError as error:
        return ({
            "recordId": recordId,
            "errors": [{"message": "Error:" + error.args[0]}]
            })

    # Now actually perform our operation
    try:
        matches = []
        matches += re.findall(regex, value['data']['text'])
    except:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Could not complete operation for record." }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "matches": matches
                }
            })