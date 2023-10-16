from io import StringIO

from auto_phylo.pipeliner.component.ParseErrorViewerDialog import ParseErrorViewerDialog
from auto_phylo.pipeliner.io import strip_lines
from auto_phylo.pipeliner.io.ParseError import ParseError
from auto_phylo.pipeliner.io.PipelineParser import PipelineParser
from fixtures.pipeline_errors import pipeline_with_multiple_errors

if __name__ == "__main__":
    parser = PipelineParser()

    text = strip_lines(pipeline_with_multiple_errors())

    try:
        parser.parse(StringIO(text))
    except ParseError as pe:
        pe = ParseError(line_errors=pe.line_errors, general_errors=["Sample general error"])

        dialog = ParseErrorViewerDialog("Pipeline error", text, pe)
        dialog.mainloop()
