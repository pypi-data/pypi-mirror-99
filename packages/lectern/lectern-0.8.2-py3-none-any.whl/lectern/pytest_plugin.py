# type: ignore


from _pytest.assertion.util import assertrepr_compare

from lectern import Document

try:
    from pytest_insta import Fmt
except ImportError:
    pass
else:
    from pathlib import Path

    from lectern import Document

    class FmtPackText(Fmt[Document]):
        extension = ".pack.txt"

        def load(self, path: Path) -> Document:
            return Document(path=path)

        def dump(self, path: Path, value: Document):
            value.save(path)

    class FmtPackMarkdown(Fmt[Document]):
        extension = ".pack.md"

        def load(self, path: Path) -> Document:
            return Document(path=path)

        def dump(self, path: Path, value: Document):
            value.save(path)

    class FmtPackMarkdownExternalFiles(Fmt[Document]):
        extension = ".pack.md_external_files"

        def load(self, path: Path) -> Document:
            return Document(path=path / "README.md")

        def dump(self, path: Path, value: Document):
            path.mkdir(exist_ok=True)
            value.save(path / "README.md", external_files=path)


def pytest_assertrepr_compare(config, op, left, right):
    if type(left) != type(right) or op != "==":
        return

    explanation = []

    if isinstance(left, Document):
        if left.assets != right.assets:
            explanation += ["", "Differing resource pack:"]
            explanation += generate_explanation(config, left.assets, right.assets)
        if left.data != right.data:
            explanation += ["", "Differing data pack:"]
            explanation += generate_explanation(config, left.data, right.data)

    if explanation:
        return [assertrepr_compare(config, op, left, right)[0]] + explanation


def generate_explanation(config, left, right):
    summary, *explanation = config.hook.pytest_assertrepr_compare(
        config=config, op="==", left=left, right=right
    )[0]

    yield f"  assert " + summary
    for line in explanation:
        yield "  " + line
