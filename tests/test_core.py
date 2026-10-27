import pytest
from compose_configuration_audit.core import audit_compose

def test_safe_image():
    r = audit_compose({"services":{"web":{"image":"nginx:1.27","ports":[{"host_ip":"127.0.0.1"}]}}})
    assert r["service_count"] == 1 and r["findings"] == []

def test_privileged_is_high():
    r = audit_compose({"services":{"web":{"privileged":True}}})
    assert r["high"] == 1

def test_docker_socket_detected():
    r = audit_compose({"services":{"web":{"volumes":[{"source":"/var/run/docker.sock"}]}}})
    assert r["findings"][0]["rule"] == "docker_socket"

def test_latest_tag_warning():
    r = audit_compose({"services":{"web":{"image":"nginx:latest"}}})
    assert r["medium"] == 1

def test_public_port_warning():
    r = audit_compose({"services":{"web":{"ports":[{"published":80,"target":80}]}}})
    assert r["findings"][0]["rule"] == "public_port_binding"

def test_host_network():
    r = audit_compose({"services":{"web":{"network_mode":"host"}}})
    assert r["high"] == 1

def test_empty_invalid_config():
    with pytest.raises(ValueError):
        audit_compose({})

def test_does_not_echo_environment():
    r = audit_compose({"services":{"db":{"environment":{"PASSWORD":"SECRET"}}}})
    assert "SECRET" not in str(r)
