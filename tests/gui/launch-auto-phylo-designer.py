from auto_phylo.pipeliner.component.AutoPhyloDesigner import AutoPhyloPipeliner
from fixtures.pipelines import advanced_configured_pipeline

if __name__ == "__main__":
    designer = AutoPhyloPipeliner(advanced_configured_pipeline())
    designer.mainloop()
