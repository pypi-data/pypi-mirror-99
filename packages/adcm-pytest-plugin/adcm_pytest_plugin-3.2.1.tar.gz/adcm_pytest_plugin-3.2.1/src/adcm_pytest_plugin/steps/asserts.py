# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Common test asserts
"""

import allure

from adcm_client.objects import BaseAPIObject


def assert_state(obj: BaseAPIObject, state):
    """
    Asserts object state to be equal to 'state' argument

    >>> some_obj = lambda: None
    >>> some_obj.state = "installed"
    >>> assert_state(some_obj, "installed") is None
    True
    >>> assert_state(some_obj, "started") # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    AssertionError:
    """
    try:
        name = obj.name
    except AttributeError:
        name = obj.__repr__
    with allure.step(f"Assert state of '{name}' to be equal to '{state}'"):
        assert obj.state == state, (
            f"Object '{name}' have unexpected status - '{obj.state}'. "
            f"Expected - '{state}'"
        )


@allure.step("Assert action result to be equal to {status}")
def assert_action_result(result: str, status: str, name=""):
    """
    Asserts action result to be equal to 'status' argument

    >>> assert_action_result("200", "200") is None
    True
    >>> assert_action_result("200", "400")
    Traceback (most recent call last):
    ...
    AssertionError: Action  finished execution with unexpected result - '200'. Expected - '400'
    >>> assert_action_result("200", "400", "some_action")
    Traceback (most recent call last):
    ...
    AssertionError: Action some_action finished execution with unexpected result - '200'. Expected - '400'
    """
    assert result == status, (
        f"Action {name} "
        f"finished execution with unexpected result - '{result}'. "
        f"Expected - '{status}'"
    )
