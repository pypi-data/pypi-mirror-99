import re
from pathlib import Path

from .preset import Preset

AUTHOR_EXTRA = re.compile(r"<.*?>|\(.*?\)|\[.*?\]")
SPACES = re.compile(r"\s+")


def join_authors(authors):
    if not authors:
        return

    if isinstance(authors, str):
        string = authors
    elif len(authors) < 2:
        string = "".join(authors)
    else:
        string = ", ".join(authors[:-1]) + f" and {authors[-1]}"

    return SPACES.sub(" ", AUTHOR_EXTRA.sub("", string)).strip().replace(" ,", ",")


class Config:
    default_source_dir = "docs"
    default_output_dir = "docs/_build"

    def __init__(
        self,
        preset="rtd",
        source_dir=None,
        output_dir=None,
        base_url=None,
        repository=None,
        verbose=False,
        project_name=None,
        project_dir=None,
        title=None,
        copyright=None,
        author=None,
        version=None,
        release=None,
        dev_server=None,
        poetry=None,
        override=None,
        section_label_depth=None,
    ):
        self.preset = preset if isinstance(preset, Preset) else Preset.get(preset)
        self.dev_server = dev_server
        self.poetry = {} if poetry is None else poetry
        self.override = override or {}
        self.override.setdefault("html_static_path", []).append(
            str(Path(__file__).resolve().with_name("_static"))
        )

        self.mkdir = []

        self.source_dir = Path(source_dir or self.default_source_dir)
        self.output_dir = Path(output_dir or self.default_output_dir)
        self.base_url = base_url
        self.verbose = verbose

        self.repository = repository or self.poetry.get("repository")

        if self.repository and not self.repository.endswith(".git"):
            self.repository += ".git"

        self.project_name = project_name or self.poetry.get("name")

        if project_dir:
            self.project_dir = project_dir
        else:
            self.try_set_project_dir()

        self.title = title or self.project_name
        self.copyright = copyright
        self.author = author or join_authors(self.poetry.get("authors"))
        self.release = release or self.poetry.get("version")
        self.version = version or self.release and ".".join(self.release.split(".")[:2])

        self.section_label_depth = section_label_depth

        self.mkdir += self.source_dir, self.output_dir

        self.set_sphinx_arguments()

        for directory in self.mkdir:
            directory.mkdir(parents=True, exist_ok=True)

        self.preset.execute(self)

    def set_sphinx_arguments(self):
        self.sphinx_project = self.title

        self.sphinx_srcdir = self.source_dir
        self.sphinx_outdir = self.output_dir / "dist"
        self.sphinx_doctreedir = self.output_dir / "doctrees"

        self.sphinx_buildername = "xml"

        self.sphinx_confdir = None
        self.sphinx_confoverrides = self.override

    def try_set_project_dir(self):
        self.project_dir = None

        if self.project_name:
            path = Path(self.project_name)

            if path.is_dir():
                self.project_dir = path
