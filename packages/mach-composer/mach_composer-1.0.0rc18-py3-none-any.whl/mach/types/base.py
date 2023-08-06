from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, List, Optional

from dataclasses_json import config, dataclass_json
from dataclasses_jsonschema import JsonSchemaMixin

from . import fields
from .components import ComponentConfig
from .general_config import GlobalConfig
from .mach import MachComposerConfig
from .sites import Site

__all__ = ["MachConfig"]


@dataclass_json
@dataclass
class MachConfig(JsonSchemaMixin):
    """Main MACH configuration object."""

    mach_composer: MachComposerConfig
    general_config: GlobalConfig = field(metadata=config(field_name="global"))
    sites: List[Site]
    components: List[ComponentConfig] = fields.list_()

    # Not used during a mach update or apply, but MACH
    # must be able to accept this attribute when parsing
    # encrypted configurations
    sops: Optional[Any] = fields.none()

    # Items that are not used in the configuration itself by set by the parser
    output_path: str = "deployments"
    file: Optional[str] = fields.none()

    @property
    def deployment_path(self) -> Path:
        return Path(self.output_path)

    def get_component(self, name: str) -> Optional[ComponentConfig]:
        for comp in self.components:
            if comp.name == name:
                return comp
        return None
