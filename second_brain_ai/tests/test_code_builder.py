import os
import tempfile

from build_system.code_builder import CodeBuilder


def test_file_generation():

    tmp_dir = tempfile.mkdtemp()

    builder = CodeBuilder(workspace_root=tmp_dir)

    outputs = [
        {
            "path": "example/test_file.py",
            "content": "print('hello world')"
        }
    ]

    files = builder.generate_files(outputs)

    assert len(files) == 1

    created_file = os.path.join(tmp_dir, files[0])

    assert os.path.exists(created_file)

    with open(created_file) as f:
        data = f.read()

    assert "hello world" in data


def test_output_validation():

    builder = CodeBuilder()

    outputs = [{"path": "file.py", "content": "x=1"}]

    assert builder.validate_outputs(outputs) is True