import base64
import hashlib
from pathlib import Path

from nbconvert.preprocessors import Preprocessor


class HighlightExercises(Preprocessor):
    """
    Any cells with the tag ``exercise`` will have the ``exercise`` css class attached to them.
    By default this highlights the output cell in yellow.
    """

    def preprocess(self, notebook, resources):
        for cell in notebook.cells:
            if "tags" in cell["metadata"]:
                if "exercise" in cell["metadata"]["tags"]:
                    cell.custom_class = "exercise"
        return notebook, resources


class PageLinks(Preprocessor):
    """
    Adds in links from one page to the next.
    The order is based on the naming of the main pages' numbers.
    i.e. ``00 Intro.ipynb` will have a next link to ``01 Foo.ipynb``.
    """

    def __init__(self, chapters, **kw):
        super().__init__(**kw)
        self.chapters = chapters

    def preprocess(self, notebook, resources):
        source_file = notebook["metadata"]["nbpretty"]["source_file"]
        files = sorted(f.stem for f in self.chapters)

        try:
            index = files.index(source_file.stem)
        except ValueError:
            # Not a chapter, i.e. an answer page or an aside
            resources["output_stem"] = source_file.stem
            return notebook, resources

        output_files = [f[3:] for f in files]  # Remove the 01, 02, 03 etc.
        output_files[0] = "index"
        resources["output_stem"] = output_files[index]

        if len(files) < 2:
            return notebook, resources

        if index == 0:
            previous_file = None
            next_file = output_files[1]
        elif index == len(output_files) - 1:
            previous_file = output_files[-2]
            next_file = None
        else:
            previous_file = output_files[index - 1]
            next_file = output_files[index + 1]

        if index == 1:
            previous_file = "index"

        source = ""
        if previous_file is not None:
            source += f'[<font size=\"5\">Previous</font>]({previous_file}.html)'
        if previous_file is not None and next_file is not None:
            source += '<font size=\"5\"> | </font>'
        if next_file is not None:
            source += f'[<font size=\"5\">Next</font>]({next_file}.html)'

        notebook.cells.append({"cell_type": "markdown", "metadata": {}, "source": source})

        return notebook, resources


class SetTitle(Preprocessor):
    """
    Based on the ``course_title`` in ``config.yaml``
    this sets the title at the top of each page and in the HTML header.
    """

    def __init__(self, course_title, **kw):
        super().__init__(**kw)
        self.course_title = course_title

    def preprocess(self, notebook, resources):
        notebook["metadata"]["course_title"] = self.course_title
        notebook["metadata"]["title"] = f"{notebook['metadata']['chapter_title']} - {self.course_title}"
        return notebook, resources


class HideWriteFileMagic(Preprocessor):
    """
    This looks for cells which start with ``%%writefile``, ``%run``, ``%cd`` or ``!`` and hides that from the output.
    For ``%%writefile`` it removes that line, sets the output prompt to the name of the file and hides the output "Overwriting foo.py".
    For ``%run foo.py`` it turns it into ``python foo.py`` and sets the prompt to ``$`` to indicate running in the terminal.
    For ``%cd`` it changes it into ``cd`` and for ``!`` it just shows the run command.
    """

    def preprocess(self, notebook, resources):
        execution_count = 0
        for cell in notebook.cells:
            if cell["source"].startswith("%%writefile"):
                file_name = cell["source"].split("\n")[0].split()[1]
                cell.metadata["writefile"] = file_name

                to_remove = len(cell["source"].split("\n")[0])
                cell["source"] = cell["source"][to_remove:]

                cell["outputs"] = []
            elif cell["source"].startswith("%run"):
                file_name = cell["source"].split()[1]
                cell.metadata["runcommand"] = ""

                cell["source"] = f"python {file_name}"
            elif cell["source"].startswith("!"):
                command = cell["source"][1:]
                if "COLUMNS=" in command:
                    command = command[len("COLUMNS=nn")+1:]
                if "venv/bin/" in command:
                    command = command[9:]
                cell.metadata["runcommand"] = ""

                cell["source"] = command
            elif cell["source"].startswith("%cd"):
                file_name = cell["source"].split()[1]
                cell.metadata["runcommand"] = ""
                cell["source"] = f"cd {file_name}"
                cell["outputs"] = []
            else:
                if "execution_count" in cell:
                    execution_count += 1
                    cell.execution_count = execution_count
        return notebook, resources


class FixLinkExtensions(Preprocessor):
    """
    Replaces all ``.ipynb`` with ``.html`` so that links continue to work.
    """

    def preprocess(self, notebook, resources):
        for cell in notebook.cells:
            # TODO Only change links to local files
            cell["source"] = cell["source"].replace(".ipynb", ".html")
        return notebook, resources


class CustomBlocks(Preprocessor):
    """
    Based on the ``custom_blocks`` list in ``config.yaml``
    it sets all cells with a tag matching a custom block name
    to be collapsible by clicking on the image that goes in the prompt.
    """

    def __init__(self, custom_blocks, **kw):
        super().__init__(**kw)
        self.custom_blocks = custom_blocks

    def preprocess(self, notebook, resources):
        "dsdf"
        if not self.custom_blocks:
            return notebook, resources

        for i, cell in enumerate(notebook.cells):
            for tag, block in self.custom_blocks.items():
                if "tags" in cell["metadata"] and tag in cell["metadata"]["tags"]:
                    cell.metadata["custom_block"] = block
                    cell.metadata["custom_block"]["id"] = i
                    cell.metadata["custom_block"]["name"] = tag
                    cell.custom_class = "outline"

        return notebook, resources


class InsertTOC(Preprocessor):
    """
    Replaces all cells with the tag ``toc`` with the table on contents,
    based on the file naming.
    """

    def __init__(self, toc_html, **kw):
        super().__init__(**kw)
        self.toc_html = toc_html

    def preprocess_cell(self, cell, resources, index):
        if "tags" in cell["metadata"] and "toc" in cell["metadata"]["tags"]:
            cell.source = self.toc_html
        return cell, resources


class UninlineCss(Preprocessor):
    """
    Moves the inlined CSS generated by nbconvert into a separate file
    which is referenced by all notebooks.
    """

    def preprocess(self, notebook, resources):
        if "files" not in resources:
            resources["files"] = {}
        for i, css in enumerate(resources["inlining"]["css"]):
            h = base64.urlsafe_b64encode(hashlib.sha1(css.encode()).digest()[:12]).decode()
            filename = Path(f"{h}.css")
            resources["inlining"]["css"][i] = f"@import '{filename}'"
            resources["files"][filename] = css
        return notebook, resources
