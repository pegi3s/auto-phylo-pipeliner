from auto_phylo.gui.component.AutoPhyloDesigner import AutoPhyloDesigner


def launch():
    designer = AutoPhyloDesigner()
    designer.minsize(width=600, height=400)
    designer.mainloop()


if __name__ == "__main__":
    launch()
