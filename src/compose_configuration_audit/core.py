from __future__ import annotations
from typing import Any

def audit_compose(config: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(config, dict) or not isinstance(config.get("services"), dict):
        raise ValueError("expected JSON from docker compose config --format json")
    findings: list[dict[str, str]] = []
    services = config["services"]
    for name, service in sorted(services.items()):
        if not isinstance(service, dict):
            findings.append({"service": str(name), "severity": "high", "rule": "invalid_service"})
            continue
        image = str(service.get("image") or "").strip()
        if image and (":" not in image.split("/")[-1] or image.endswith(":latest")):
            findings.append({"service": str(name), "severity": "medium", "rule": "unpinned_image"})
        if service.get("privileged") is True:
            findings.append({"service": str(name), "severity": "high", "rule": "privileged"})
        if service.get("network_mode") == "host":
            findings.append({"service": str(name), "severity": "high", "rule": "host_network"})
        for mount in service.get("volumes") or []:
            source = (mount.get("source", "") if isinstance(mount, dict) else str(mount).split(":")[0])
            if source == "/var/run/docker.sock":
                findings.append({"service": str(name), "severity": "high", "rule": "docker_socket"})
        for port in service.get("ports") or []:
            if isinstance(port, dict):
                bound = str(port.get("host_ip") or "0.0.0.0")
            else:
                value = str(port)
                bound = "127.0.0.1" if value.startswith("127.0.0.1:") else "0.0.0.0"
            if bound in {"0.0.0.0", "::", ""}:
                findings.append({"service": str(name), "severity": "medium", "rule": "public_port_binding"})
    return {"service_count": len(services), "findings": findings,
            "high": sum(f["severity"] == "high" for f in findings),
            "medium": sum(f["severity"] == "medium" for f in findings)}
