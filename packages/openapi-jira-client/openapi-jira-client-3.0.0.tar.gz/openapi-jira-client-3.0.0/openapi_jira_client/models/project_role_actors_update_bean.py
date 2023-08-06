from typing import Any, Dict, Type, TypeVar, Union, cast

import attr

from ..models.project_role_actors_update_bean_categorised_actors import ProjectRoleActorsUpdateBeanCategorisedActors
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectRoleActorsUpdateBean")


@attr.s(auto_attribs=True)
class ProjectRoleActorsUpdateBean:
    """  """

    id: Union[Unset, int] = UNSET
    categorised_actors: Union[ProjectRoleActorsUpdateBeanCategorisedActors, Unset] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        categorised_actors: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.categorised_actors, Unset):
            categorised_actors = self.categorised_actors.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if categorised_actors is not UNSET:
            field_dict["categorisedActors"] = categorised_actors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        categorised_actors: Union[ProjectRoleActorsUpdateBeanCategorisedActors, Unset] = UNSET
        _categorised_actors = d.pop("categorisedActors", UNSET)
        if not isinstance(_categorised_actors, Unset):
            categorised_actors = ProjectRoleActorsUpdateBeanCategorisedActors.from_dict(_categorised_actors)

        project_role_actors_update_bean = cls(
            id=id,
            categorised_actors=categorised_actors,
        )

        return project_role_actors_update_bean
