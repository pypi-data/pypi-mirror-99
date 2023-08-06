code_with_import_and_assignment = """
from sym.sdk.annotations import reducer
import datetime
@reducer
def get_action_time(input)->str:
    print(f"The time right now is: {datetime.datetime.utcnow()}")

get_action_time(None)
"""


class TestReducer:
    def test_reducer_using_global_namespace(self):
        """Run reducer using global namespace
        Exec runs in a local namespace, so imports won't work.  Telling exec
        to use globals allows the imports and code to work as we'd expect
        """
        reducer_object = compile(code_with_import_and_assignment, "<string>", "exec")
        exec(reducer_object, globals())
