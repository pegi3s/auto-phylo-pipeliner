import json
from importlib import resources

import auto_phylo
from auto_phylo.gui.component.AutoPhyloDesigner import AutoPhyloDesigner
from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.Commands import Commands


def launch():
    with resources.open_text(auto_phylo, "commands.json", "utf-8") as file:
        commands = json.load(file)

    designer = AutoPhyloDesigner(Commands(Command(**data) for data in commands))
    designer.mainloop()


if __name__ == "__main__":
    launch()
