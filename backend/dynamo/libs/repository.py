import json


class Responses:
    Created = {"statusCode": 201, "body": "Created!\n"}
    OK = {"statusCode": 200, "body": "OK\n"}


class put_context:
    """ Thanks to: 
        https://stackoverflow.com/questions/877709/how-should-i-return-interesting-values-from-a-with-statement
    """

    def __init__(self):
        self.response = Responses.Created

    def __enter__(*args):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.response = {
                "statusCode": 500,
                "body": json.dumps(
                    {"message": "Creation failed: {}".format(str(exc_value)),}
                ),
            }
        return True


"""
@contextmanager
def put_context():
    try:
        yield
        print("Created OK!")
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Creation failed: {}".format(str(err)),
            }),
        }
"""


def put_item_into_table(table, input_dict):
    print("Putting...")
    table.put_item(Item=input_dict)
    print("Put ok!")
