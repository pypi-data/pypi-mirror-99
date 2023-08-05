# dbnomics-fetcher-ops -- Manage DBnomics fetchers
# By: Christophe Benz <christophe.benz@cepremap.org>
#
# Copyright (C) 2020 Cepremap
# https://git.nomics.world/dbnomics/dbnomics-fetcher-ops
#
# dbnomics-fetcher-ops is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# dbnomics-fetcher-ops is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from typing import Dict, List

from pydantic import BaseModel, Field


class ScheduleDef(BaseModel):
    cron: str
    timezone: str


class FetcherDef(BaseModel):
    provider_code: str
    provider_slug: str
    schedules: List[ScheduleDef]
    legacy_pipeline: bool = False


class ProjectRef(BaseModel):
    group: str
    name: str
    variables: Dict[str, str] = Field(default_factory=dict)


class GitLab(BaseModel):
    fetcher: ProjectRef
    json_data: ProjectRef
    source_data: ProjectRef


class PipelineDef(BaseModel):
    template: dict


class FetcherMetadata(BaseModel):
    version: int

    fetchers: List[FetcherDef]
    gitlab: GitLab
    pipeline: PipelineDef
