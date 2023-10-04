from auto_phylo.gui.component.AutoPhyloDesigner import AutoPhyloDesigner
from fixtures.pipelines import advanced_configured_pipeline

if __name__ == "__main__":
    designer = AutoPhyloDesigner(advanced_configured_pipeline())
    designer.mainloop()
