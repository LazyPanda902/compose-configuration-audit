import json
from compose_configuration_audit.cli import main

def test_medium_warning_fails_only_when_strict(tmp_path, capsys):
    p = tmp_path / "compose.json"
    p.write_text(json.dumps({"services":{"web":{"image":"nginx:latest"}}}))
    assert main([str(p)]) == 0
    assert main(["--strict", str(p)]) == 1
    assert "unpinned_image" in capsys.readouterr().out

def test_strict_accepts_clean_configuration(tmp_path):
    p = tmp_path / "compose.json"
    p.write_text(json.dumps({"services":{"web":{"image":"nginx:1.27"}}}))
    assert main(["--strict", str(p)]) == 0
