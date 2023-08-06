# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
# pylint:disable=missing-module-docstring
from typing import List

from gql import (
    Client,
    gql,
)
from qctrlcommons.exceptions import QctrlGqlException

from qctrl.builders.custom_environment import QctrlGraphQLEnvironment
from qctrl.queries.base import BaseQuery

MAX_ACTION_RECORDS = 50000

_ACTION_EXPORT = """
    query run_action_export($limit: Int, $filterBy: ActionFilter){
        actions(limit: $limit, filterBy: $filterBy){
            actions {
                user {
                  username
                }
                modelId
                name
                status
                errors {
                    exception
                    traceback
                }
                createdAt
                updatedAt
                terminatedAt
                runtime
            }
            errors {
                message
            }
        }
    }
    """


class ActionExportQuery(BaseQuery):
    """
    Class for executing the `actions` query to extract data from action table.
    """

    def __init__(
        self,
        client: Client,
        env: QctrlGraphQLEnvironment,
        start_date: str,
        end_date: str,
        ignore_test_users: bool,
    ):
        """

        Parameters
        ----------
        client: Client
            The graphql client.
        env: QctrlGraphQLEnvironment
            Runtime graphql environment.
        start_date: str
            The date begin.
        end_date: ste
            The date till.
        ignore_test_users: bool
            Flag to ignore the action records created by test users
        """
        self.start_date = start_date
        self.end_date = end_date
        self.ignore_test_users = ignore_test_users
        super().__init__(client, env)

    def __call__(self) -> List:
        """Executes the `actions` mutation.

        Returns
        -------
        List
            List of actions result

        Raises
        ------
        QctrlGqlException
            If something wrong happens with the query or authentication.
        """
        filter_by = {
            "createdAt": {"range": [self.start_date, self.end_date]},
            "ignoreTestUsers": self.ignore_test_users,
        }
        result = self.execute_query(
            gql(_ACTION_EXPORT),
            variable_values={"limit": MAX_ACTION_RECORDS, "filterBy": filter_by},
        )

        if result.get("errors"):
            raise QctrlGqlException(result["errors"])

        # custom errors handling
        if result["actions"]["errors"]:
            raise QctrlGqlException(result["actions"]["errors"])

        return result["actions"]["actions"]
