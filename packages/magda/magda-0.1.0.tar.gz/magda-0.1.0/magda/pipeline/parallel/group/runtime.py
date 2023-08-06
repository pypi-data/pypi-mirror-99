from __future__ import annotations

import asyncio
from uuid import UUID
from typing import List, Iterable

from magda.module.module import Module
from magda.pipeline.parallel.group.actor import Actor
from magda.pipeline.parallel.group.actor_pool import ParallelActorPool
from magda.pipeline.parallel.group.state_type import StateType


class GroupRuntime:
    def __init__(
        self,
        *,
        name: str,
        modules: List[Module],
        dependent_modules: List[Module],
        dependent_modules_nonregular: List[Module],
        replicas: int = 1,
        state_type: StateType = True,
        options={},
    ):
        self.name = name
        self._modules = modules
        self._state_type = state_type
        self.dependencies = set([m.group for m in dependent_modules])
        self.module_dependencies = set([m.name for m in dependent_modules])
        self.dependencies_nonregular = set([m.group for m in dependent_modules_nonregular])
        self.module_dependencies_nonregular = set([m.name for m in dependent_modules_nonregular])
        self.pool = ParallelActorPool([
            Actor.options(**options).remote(name, state_type, modules)
            for _ in range(replicas)
        ])

    @property
    def modules(self) -> List[Module]:
        return self._modules

    @property
    def is_replicated(self) -> bool:
        return self.pool.replicas > 1

    @property
    def state_type(self) -> bool:
        return self._state_type

    def fulfills(self, names: Iterable[str]) -> bool:
        return set(names).issuperset(self.module_dependencies)

    async def run(self, job_id: UUID, request, results, is_regular_runtime):
        return asyncio.ensure_future(
            self.pool.run(
                job_id=job_id,
                request=request,
                results=results,
                is_regular_runtime=is_regular_runtime
            )
        )

    async def teardown(self):
        await self.pool.teardown()
