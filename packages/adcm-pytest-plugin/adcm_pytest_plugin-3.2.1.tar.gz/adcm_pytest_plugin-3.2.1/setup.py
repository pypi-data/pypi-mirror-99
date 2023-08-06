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

from setuptools import setup, find_packages

setup(
    name="adcm_pytest_plugin",
    description="pytest adcm launch arguments" " and fixtures library",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    version="3.2.1",
    # the following makes a plugin available to pytest
    entry_points={"pytest11": ["adcm_pytest_plugin = adcm_pytest_plugin.plugin"]},
    # custom PyPI classifier for pytest plugins
    install_requires=[
        "pytest",
        "docker",
        "adcm_client>=2020.02.11.12",
        "allure-pytest",
        "requests",
        "version_utils",
        "ifaddr",
        "retry",
        "deprecated",
    ],
    classifiers=["Framework :: Pytest"],
)
