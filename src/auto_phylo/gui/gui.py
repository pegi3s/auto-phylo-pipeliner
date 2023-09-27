from auto_phylo.gui import load_commands
from auto_phylo.gui.component.AutoPhyloDesigner import AutoPhyloDesigner


def launch():
    designer = AutoPhyloDesigner(load_commands())
    designer.mainloop()


if __name__ == "__main__":
    launch()
