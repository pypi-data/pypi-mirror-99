# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
from typing import List, Tuple

import click

from lean.components.util.logger import Logger
from lean.models.api import QCParameter
from lean.models.logger import Option
from lean.models.optimizer import (OptimizationConstraint, OptimizationConstraintOperator, OptimizationExtremum,
                                   OptimizationParameter, OptimizationTarget)
from lean.models.pydantic import WrappedBaseModel


class NodeType(WrappedBaseModel):
    name: str
    ram: int
    cores: int
    price: float
    min_nodes: int
    max_nodes: int
    default_nodes: int


class OptimizerConfigManager:
    """The OptimizationConfigurer contains methods to interactively configure parts of the optimizer."""

    def __init__(self, logger: Logger) -> None:
        """Creates a new OptimizationConfigurer instance.

        :param logger: the logger to use when printing messages
        """
        self._logger = logger

        # The targets that are available in the cloud
        self.available_targets = [
            ("TotalPerformance.PortfolioStatistics.SharpeRatio", "Sharpe Ratio"),
            ("TotalPerformance.PortfolioStatistics.CompoundingAnnualReturn", "Compounding Annual Return"),
            ("TotalPerformance.PortfolioStatistics.ProbabilisticSharpeRatio", "Probabilistic Sharpe Ratio"),
            ("TotalPerformance.PortfolioStatistics.Drawdown", "Drawdown")
        ]

        # The nodes that are available in the cloud
        # Copied from ViewsOptimization.NodeTypes in js/views/ViewsOptimization.js
        self._available_nodes = [
            NodeType(name="O2-8",
                     ram=8,
                     cores=2,
                     price=0.15,
                     min_nodes=1,
                     max_nodes=24,
                     default_nodes=12),
            NodeType(name="O4-12",
                     ram=12,
                     cores=4,
                     price=0.3,
                     min_nodes=1,
                     max_nodes=12,
                     default_nodes=6),
            NodeType(name="O8-16",
                     ram=16,
                     cores=8,
                     price=0.6,
                     min_nodes=1,
                     max_nodes=6,
                     default_nodes=3)
        ]

    def configure_strategy(self, cloud: bool) -> str:
        """Asks the user for the optimization strategy to use.

        :param cloud: True if the optimization will be ran in the cloud, False if not
        :return: the class name of the optimization strategy to use
        """
        options = [
            Option(id="QuantConnect.Optimizer.Strategies.GridSearchOptimizationStrategy", label="Grid Search")
        ]

        if not cloud:
            options.append(
                Option(id="QuantConnect.Optimizer.Strategies.EulerSearchOptimizationStrategy", label="Euler Search")
            )

        return self._logger.prompt_list("Select the optimization strategy to use", options)

    def configure_target(self) -> OptimizationTarget:
        """Asks the user for the optimization target.

        :return: the chosen optimization target
        """
        # Create a list of options containing a "<target> (min)" and "<target> (max)" option for every target
        options = list(itertools.product(self.available_targets,
                                         [OptimizationExtremum.Minimum, OptimizationExtremum.Maximum]))
        options = [Option(id=OptimizationTarget(target=option[0][0], extremum=option[1]),
                          label=f"{option[0][1]} ({option[1]})") for option in options]

        return self._logger.prompt_list("Select an optimization target", options)

    def configure_parameters(self, project_parameters: List[QCParameter], cloud: bool) -> List[OptimizationParameter]:
        """Asks the user which parameters need to be optimized and with what constraints.

        :param project_parameters: the parameters of the project that will be optimized
        :param cloud: True if the optimization will be ran in the cloud, False if not
        :return: the chosen optimization parameters
        """
        results: List[OptimizationParameter] = []

        for parameter in project_parameters:
            if cloud and len(results) == 2:
                self._logger.warn(f"You can optimize up to 2 parameters in the cloud, skipping '{parameter.key}'")
                continue

            if not click.confirm(f"Should the '{parameter.key}' parameter be optimized?", default=True):
                continue

            minimum = click.prompt(f"Minimum value for '{parameter.key}'", type=click.FLOAT)
            maximum = click.prompt(f"Maximum value for '{parameter.key}'", type=click.FloatRange(min=minimum))
            step_size = click.prompt(f"Step size for '{parameter.key}'", type=click.FloatRange(min=0.0), default=1.0)

            results.append(OptimizationParameter(name=parameter.key, min=minimum, max=maximum, step=step_size))

        return results

    def configure_constraints(self) -> List[OptimizationConstraint]:
        """Asks the user for the optimization constraints.

        :return: the chosen optimization constraints
        """
        self._logger.info("Constraints can be used to filter out backtests from the results")
        self._logger.info("When a backtest doesn't comply with the constraints it is dropped from the results")
        self._logger.info("Example constraint: Drawdown < 0.25 (Drawdown less than 25%)")

        results: List[OptimizationConstraint] = []

        while True:
            results_str = ", ".join([str(result) for result in results])
            results_str = results_str or "None"
            self._logger.info(f"Current constraints: {results_str}")

            if not click.confirm("Do you want to add a constraint?", default=False):
                return results

            target_options = [Option(id=target[0], label=target[1]) for target in self.available_targets]
            target = self._logger.prompt_list("Select a constraint target", target_options)

            operator = self._logger.prompt_list("Select a constraint operator (<value> will be asked after this)", [
                Option(id=OptimizationConstraintOperator.Less, label="Less than <value>"),
                Option(id=OptimizationConstraintOperator.LessOrEqual, label="Less than or equal to <value>"),
                Option(id=OptimizationConstraintOperator.Greater, label="Greater than <value>"),
                Option(id=OptimizationConstraintOperator.GreaterOrEqual, label="Greater than or equal to <value>"),
                Option(id=OptimizationConstraintOperator.Equals, label="Equal to <value>"),
                Option(id=OptimizationConstraintOperator.NotEqual, label="Not equal to <value>")
            ])

            value = click.prompt("Set the <value> for the selected operator", type=click.FLOAT)

            results.append(OptimizationConstraint(**{"target": target, "operator": operator, "target-value": value}))

    def configure_node(self) -> Tuple[NodeType, int]:
        """Asks the user for the node type and number of parallel nodes to run on.

        :return: the type of the node and the amount of parallel nodes to run
        """
        node_options = [
            Option(id=node, label=f"{node.name} ({node.cores} cores, {node.ram} GB RAM) @ ${node.price:.2f} per hour")
            for node in self._available_nodes
        ]

        node = self._logger.prompt_list("Select the optimization node type", node_options)
        parallel_nodes = click.prompt(f"How many nodes should run in parallel ({node.min_nodes}-{node.max_nodes})",
                                      type=click.IntRange(min=node.min_nodes, max=node.max_nodes),
                                      default=node.default_nodes)

        return node, parallel_nodes
