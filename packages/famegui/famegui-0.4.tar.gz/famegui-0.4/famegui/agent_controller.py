import logging
import typing

from famegui import models, colorpalette


class AgentController(models.Agent):
    """ Controller attached to a FAME Agent to sync it with the views """

    def __init__(self, agent: models.Agent):
        self.model = agent
        self.tree_item = None
        self.scene_item = None

    @property
    def id(self) -> int:
        return self.model.id

    @property
    def id_str(self) -> str:
        return self.model.id_str

    @property
    def type_name(self) -> str:
        return self.model.type_name

    @property
    def attributes(self) -> typing.Dict[str, str]:
        return self.model.attributes

    @property
    def tooltip_text(self) -> str:
        text = "<font size='4'><b>{}</b></font>".format(self.model.type_name)

        text += "<table border=0 cellpadding=2 style='border-collapse: collapse'><tbody>"
        text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(
            "ID", self.model.id_str)
        for k, v in self.model.attributes.items():
            text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(k, v)

        text += "</tbody></table>"
        return text

    @property
    def svg_color(self) -> str:
        return colorpalette.color_for_agent_type(self.type_name)

    @property
    def x(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[0]

    @property
    def y(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[1]
