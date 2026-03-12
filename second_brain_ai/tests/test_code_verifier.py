import tempfile
import os

from build_system.code_verifier import CodeVerifier


def test_syntax_verification():

    verifier = CodeVerifier()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py")

    with open(tmp.name, "w") as f:
        f.write("x = 1\n")

    assert verifier.verify_syntax([tmp.name]) is True


def test_import_verification():

    verifier = CodeVerifier()

    assert verifier.verify_imports(["math"]) is True