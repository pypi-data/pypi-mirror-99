# Copyright 2020-2021 Axis Communications AB.
#
# For a full list of individual contributors, please see the commit history.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""ETR test runner module."""
import time
import os
import logging
from pprint import pprint

from etos_test_runner.lib.graphql import request_test_suite_started
from etos_test_runner.lib.iut_monitoring import IutMonitoring
from etos_test_runner.lib.executor import Executor
from etos_test_runner.lib.workspace import Workspace
from etos_test_runner.lib.log_area import LogArea


class TestRunner:
    """Test runner for ETOS."""

    logger = logging.getLogger("ETR")

    def __init__(self, iut, etos):
        """Initialize.

        :param iut: IUT to execute tests on.
        :type iut: :obj:`etr.lib.iut.Iut`
        :param etos: ETOS library
        :type etos: :obj:`etos_lib.etos.ETOS`
        """
        self.etos = etos
        self.iut = iut
        self.config = self.etos.config.get("test_config")

        self.log_area = LogArea(self.etos)
        self.iut_monitoring = IutMonitoring(self.iut)
        self.issuer = {"name": "ETOS Test Runner"}

    def test_suite_started(self):
        """Publish a test suite started event.

        :return: Reference to test suite started.
        :rtype: :obj:`eiffel.events.base_event.BaseEvent`
        """
        suite_name = self.config.get("name")
        categories = ["Regression test_suite", "Sub suite"]
        categories.append(self.iut.identity.name)
        livelogs = self.config.get("log_area", {}).get("livelogs")

        return self.etos.events.send_test_suite_started(
            suite_name,
            links={"CONTEXT": self.etos.config.get("context")},
            categories=categories,
            types=["FUNCTIONAL"],
            liveLogs=[{"name": "console", "uri": livelogs}],
        )

    def main_suite_id(self, activity_id):
        """Get the eiffel event id of the mainsuite linked form the activity triggered event.

        :param activity_id: Id of the activity linked to the main suite
        :type activity_id: str
        :return: Id of the main suite linked from the activity triggered event
        :rtype: str
        """
        for test_suite_started in request_test_suite_started(self.etos, activity_id):
            if not "Sub suite" in test_suite_started["data"]["testSuiteCategories"]:
                return test_suite_started["meta"]["id"]
        raise Exception("Missing main suite events, exiting!")

    def confidence_level(self, test_results, test_suite_started):
        """Publish confidence level modified event.

        :param test_results: Results of the test suite.
        :type test_results: bool
        :param test_suite_started: Test suite started event to use as Cause for this confidence.
        :type test_suite_started: :obj:`eiffellib.events.EiffelTestSuiteStartedEvent`
        """
        confidence = self.etos.events.send_confidence_level_modified(
            "{}_OK".format(self.config.get("name")),
            "SUCCESS" if test_results else "FAILURE",
            links={
                "CONTEXT": self.etos.config.get("context"),
                "CAUSE": test_suite_started,
                "SUBJECT": self.config.get("artifact"),
            },
            issuer=self.issuer,
        )
        print(confidence.pretty)

    def environment(self, context):
        """Send out which environment we're executing within.

        :param context: Context where this environment is used.
        :type context: str
        """
        # TODO: Get this from prepare
        if os.getenv("HOSTNAME") is not None:
            self.etos.events.send_environment_defined(
                "ETR Hostname",
                links={"CONTEXT": context},
                host={"name": os.getenv("HOSTNAME"), "user": "etos"},
            )

    def run_tests(self, workspace):
        """Execute test recipes within a test executor.

        :param workspace: Which workspace to execute test suite within.
        :type workspace: :obj:`etr.lib.workspace.Workspace`
        :return: Result of test execution.
        :rtype: bool
        """
        recipes = self.config.get("recipes")
        result = True
        for num, test in enumerate(recipes):
            self.logger.info("Executing test %s/%s", num + 1, len(recipes))
            with Executor(test, self.iut, self.etos) as executor:
                self.logger.info("Starting test '%s'", executor.test_name)
                executor.execute(workspace)

                if not executor.result:
                    result = executor.result
                self.logger.info("Test finished. Result: %s.", executor.result)
        return result

    def outcome(self, result, executed, description):
        """Get outcome from test execution.

        :param result: Result of execution.
        :type result: bool
        :param executed: Whether or not tests have successfully executed.
        :type executed: bool
        :param description: Optional description.
        :type description: str
        :return: Outcome of test execution.
        :rtype: dict
        """
        if executed:
            conclusion = "SUCCESSFUL"
            verdict = "PASSED" if result else "FAILED"
            self.logger.info(
                "Tests executed successfully. "
                "Verdict set to '%s' due to result being '%s'",
                verdict,
                result,
            )
        else:
            conclusion = "FAILED"
            verdict = "INCONCLUSIVE"
            self.logger.info(
                "Tests did not execute successfully. " "Setting verdict to '%s'",
                verdict,
            )

        suite_name = self.config.get("name")
        if not description and not result:
            self.logger.info(
                "No description but result is a failure. " "At least some tests failed."
            )
            description = "At least some {} tests failed.".format(suite_name)
        elif not description and result:
            self.logger.info(
                "No description and result is a success. "
                "All tests executed successfully."
            )
            description = "All {} tests completed successfully.".format(suite_name)
        else:
            self.logger.info("Description was set. Probably due to an exception.")
        return {
            "verdict": verdict,
            "description": description,
            "conclusion": conclusion,
        }

    def execute(self):  # pylint:disable=too-many-branches
        """Execute all tests in test suite.

        :return: Result of execution. Linux exit code.
        :rtype: int
        """
        self.logger.info("Send test suite started event.")
        test_suite_started = self.test_suite_started()
        sub_suite_id = test_suite_started.meta.event_id
        main_suite_id = self.main_suite_id(self.etos.config.get("context"))
        self.logger.info("Send test environment events.")
        self.environment(sub_suite_id)
        self.etos.config.set("main_suite_id", main_suite_id)
        self.etos.config.set("sub_suite_id", sub_suite_id)

        result = True
        description = None
        try:
            with Workspace(self.log_area) as workspace:
                self.logger.info("Start IUT monitoring.")
                self.iut_monitoring.start_monitoring()
                self.logger.info("Starting test executor.")
                result = self.run_tests(workspace)
                executed = True
        except Exception as exception:  # pylint:disable=broad-except
            result = False
            executed = False
            description = str(exception)
            raise
        finally:
            self.logger.info("Stop IUT monitoring.")
            self.iut_monitoring.stop_monitoring()

            self.logger.info("Figure out test outcome.")
            outcome = self.outcome(result, executed, description)
            pprint(outcome)

            self.logger.info("Send test suite finished and confidence events.")
            self.etos.events.send_test_suite_finished(
                test_suite_started,
                links={"CONTEXT": self.etos.config.get("context")},
                outcome=outcome,
                persistentLogs=self.log_area.persistent_logs,
            )
            self.confidence_level(result, test_suite_started)
        timeout = time.time() + 30
        self.logger.info("Waiting for eiffel publisher to deliver events (30s).")
        # pylint:disable=len-as-condition, protected-access
        while len(self.etos.publisher._deliveries):
            if time.time() > timeout:
                raise Exception("Eiffel publisher did not deliver all eiffel events.")
            time.sleep(1)
        self.logger.info("Tests finished executing.")
        return 0 if result else outcome
