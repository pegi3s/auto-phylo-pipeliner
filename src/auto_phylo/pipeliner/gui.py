from auto_phylo.pipeliner.component.AutoPhyloPipeliner import AutoPhyloPipeliner


def launch():
    designer = AutoPhyloPipeliner()
    designer.minsize(width=600, height=400)
    designer.mainloop()


if __name__ == "__main__":
    launch()
