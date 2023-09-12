import json

from auto_phylo.gui.component.AutoPhyloDesigner import AutoPhyloDesigner
from auto_phylo.gui.model.Command import Command
from auto_phylo.gui.model.Commands import Commands


def launch():
    with open("commands.json", "r") as file:
        commands = json.load(file)

    designer = AutoPhyloDesigner(Commands(Command(**data) for data in commands))
    designer.mainloop()


if __name__ == "__main__":
    launch()
