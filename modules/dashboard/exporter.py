"""
Dashboard Exporter

Export dashboard analysis results.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from core.logger import success, warning

from .constants import (
    DASHBOARD_DIR,
    DASHBOARD_HTML,
    DASHBOARD_JSON,
    DASHBOARD_SUMMARY,
    DASHBOARD_TXT,
)

# ==========================================================
# Output Directory
# ==========================================================


def create_output_directory() -> None:
    """
    Create dashboard output directory.
    """

    DASHBOARD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


# ==========================================================
# Write Text
# ==========================================================


def write_text(
    output_file: Path,
    lines: list[str],
) -> Path:
    """
    Write text report.

    Args:
        output_file:
            Destination file.

        lines:
            Report lines.

    Returns:
        Output file path.
    """

    try:

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

    return output_file


# ==========================================================
# Write JSON
# ==========================================================


def write_json(
    output_file: Path,
    data: Any,
) -> Path:
    """
    Write JSON report.

    Args:
        output_file:
            Destination file.

        data:
            Serializable object.

    Returns:
        Output file path.
    """

    try:

        with output_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
                default=str,
            )

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

    return output_file


# ==========================================================
# Write HTML
# ==========================================================


def write_html(
    output_file: Path,
    html: str,
) -> Path:
    """
    Write HTML dashboard.

    Args:
        output_file:
            Destination file.

        html:
            HTML content.

    Returns:
        Output file path.
    """

    try:

        output_file.write_text(
            html,
            encoding="utf-8",
        )

        success(f"Saved {output_file}")

    except OSError as error:

        warning(f"{output_file}: {error}")

    return output_file


# ==========================================================
# Export JSON
# ==========================================================


def export_json(
    analysis: dict[str, Any],
) -> Path:
    """
    Export JSON report.
    """

    return write_json(
        DASHBOARD_JSON,
        analysis,
    )


# ==========================================================
# Export TXT
# ==========================================================


def export_txt(
    analysis: dict[str, Any],
) -> Path:
    """
    Export text report.
    """

    statistics = analysis["statistics"]

    results = analysis["results"]

    lines = [
        "Dashboard",
        "=" * 80,
        "",
        f"Target             : {statistics['target']}",
        f"Modules            : {statistics['modules']}",
        f"Completed Modules  : {statistics['completed_modules']}",
        f"Failed Modules     : {statistics['failed_modules']}",
        f"Findings           : {statistics['findings']}",
        "",
        "Executed Modules",
        "-" * 80,
    ]

    for module in results.get(
        "module_names",
        [],
    ):

        lines.append(f"• {module}")

    return write_text(
        DASHBOARD_TXT,
        lines,
    )


# ==========================================================
# Export Summary
# ==========================================================


def export_summary(
    analysis: dict[str, Any],
) -> Path:
    """
    Export summary report.
    """

    statistics = analysis["statistics"]

    lines = [
        "Dashboard Summary",
        "=" * 40,
        f"Target             : {statistics['target']}",
        f"Modules            : {statistics['modules']}",
        f"Completed Modules  : {statistics['completed_modules']}",
        f"Failed Modules     : {statistics['failed_modules']}",
        f"Findings           : {statistics['findings']}",
    ]

    return write_text(
        DASHBOARD_SUMMARY,
        lines,
    )


# ==========================================================
# Build CSS
# ==========================================================


def _build_css() -> str:
    """
    Build dashboard CSS.

    Returns:
        CSS stylesheet.
    """

    return """
<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

:root{

    --background:#0f172a;
    --surface:#1e293b;
    --border:#334155;

    --text:#e2e8f0;
    --muted:#94a3b8;

    --primary:#3b82f6;
    --success:#22c55e;
    --danger:#ef4444;

}

body{

    background:var(--background);

    color:var(--text);

    font-family:
        Inter,
        "Segoe UI",
        Arial,
        sans-serif;

    padding:40px;

}

.container{

    max-width:1440px;

    margin:auto;

}

h1{

    font-size:38px;

    margin-bottom:8px;

}

.subtitle{

    color:var(--muted);

    margin-bottom:32px;

}

.grid{

    display:grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(220px,1fr)
        );

    gap:20px;

}

.card{

    background:var(--surface);

    border:1px solid var(--border);

    border-radius:14px;

    padding:22px;

    transition:
        transform .2s ease,
        box-shadow .2s ease;

}

.card:hover{

    transform:translateY(-4px);

    box-shadow:
        0 12px 24px
        rgba(0,0,0,.25);

}

.card h3{

    color:var(--muted);

    font-size:14px;

    font-weight:500;

    margin-bottom:10px;

}

.card h2{

    font-size:34px;

}

.section{

    margin-top:50px;

}

.section h2{

    margin-bottom:18px;

}

table{

    width:100%;

    border-collapse:collapse;

}

th{

    background:var(--surface);

    text-align:left;

    padding:14px;

}

td{

    padding:14px;

    border-bottom:
        1px solid var(--border);

}

tbody tr:hover{

    background:#273449;

}

.status-success{

    color:var(--success);

    font-weight:bold;

}

.status-failed{

    color:var(--danger);

    font-weight:bold;

}

.progress{

    width:100%;

    height:10px;

    background:#334155;

    border-radius:20px;

    overflow:hidden;

    margin-top:14px;

}

.progress-bar-success{

    height:100%;

    background:var(--success);

}

.progress-bar-danger{

    height:100%;

    background:var(--danger);

}

hr{

    border:none;

    border-top:1px solid var(--border);

    margin:25px 0;

}

footer{

    margin-top:60px;

    text-align:center;

    color:var(--muted);

    line-height:1.8;

}

@media (max-width:768px){

    body{

        padding:20px;

    }

    h1{

        font-size:30px;

    }

    .card h2{

        font-size:26px;

    }

}

</style>
"""


# ==========================================================
# Build Header
# ==========================================================


def _build_header(
    statistics: dict,
) -> str:
    """
    Build dashboard header.

    Args:
        statistics:
            Dashboard statistics.

    Returns:
        HTML header.
    """

    return f"""
<div class="container">

<header>

<h1>

Recon Automation Framework Dashboard

</h1>

<p class="subtitle">

Professional Modular Reconnaissance Framework

</p>

<hr>

<table>

<tr>

<th style="width:220px;">
Property
</th>

<th>
Value
</th>

</tr>

<tr>

<td>
Target
</td>

<td>

<strong>

{statistics["target"]}

</strong>

</td>

</tr>

<tr>

<td>
Generated
</td>

<td>

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

</td>

</tr>

<tr>

<td>
Framework
</td>

<td>

Recon Automation Framework

</td>

</tr>

<tr>

<td>
Version
</td>

<td>

v1.0.0

</td>

</tr>

</table>

</header>

"""


# ==========================================================
# Build Summary Cards
# ==========================================================


def _build_summary_cards(
    statistics: dict,
) -> str:
    """
    Build dashboard summary cards.

    Args:
        statistics:
            Dashboard statistics.

    Returns:
        Summary card section.
    """

    return f"""
<div class="grid">

<div class="card">

<h3>

🎯 Target

</h3>

<h2>

{statistics["target"]}

</h2>

</div>


<div class="card">

<h3>

📦 Modules

</h3>

<h2>

{statistics["modules"]}

</h2>

</div>


<div class="card">

<h3>

✅ Completed

</h3>

<h2 class="status-success">

{statistics["completed_modules"]}

</h2>

</div>


<div class="card">

<h3>

❌ Failed

</h3>

<h2 class="status-failed">

{statistics["failed_modules"]}

</h2>

</div>


<div class="card">

<h3>

🔍 Findings

</h3>

<h2>

{statistics["findings"]}

</h2>

</div>

</div>
"""


# ==========================================================
# Build Execution Summary
# ==========================================================


def _build_execution_summary(
    statistics: dict,
) -> str:
    """
    Build execution summary section.

    Args:
        statistics:
            Dashboard statistics.

    Returns:
        HTML execution summary.
    """

    success_rate = round(
        (
            statistics["completed_modules"]
            / max(
                statistics["modules"],
                1,
            )
        )
        * 100,
        1,
    )

    failure_rate = round(
        (
            statistics["failed_modules"]
            / max(
                statistics["modules"],
                1,
            )
        )
        * 100,
        1,
    )

    return f"""
<div class="section">

<h2>

Execution Summary

</h2>

<table>

<thead>

<tr>

<th style="width:40%;">

Property

</th>

<th>

Value

</th>

</tr>

</thead>

<tbody>

<tr>

<td>

Total Modules

</td>

<td>

{statistics["modules"]}

</td>

</tr>

<tr>

<td>

Completed Modules

</td>

<td class="status-success">

{statistics["completed_modules"]}

</td>

</tr>

<tr>

<td>

Failed Modules

</td>

<td class="status-failed">

{statistics["failed_modules"]}

</td>

</tr>

<tr>

<td>

Total Findings

</td>

<td>

{statistics["findings"]}

</td>

</tr>

<tr>

<td>

Success Rate

</td>

<td>

{success_rate}%

<div class="progress">

<div
class="progress-bar-success"
style="width:{success_rate}%;">
</div>

</div>

</td>

</tr>

<tr>

<td>

Failure Rate

</td>

<td>

{failure_rate}%

<div class="progress">

<div
class="progress-bar-danger"
style="width:{failure_rate}%;">
</div>

</div>

</td>

</tr>

</tbody>

</table>

</div>
"""


# ==========================================================
# Build Module Status
# ==========================================================


def _build_module_status(
    modules: list[str],
) -> str:
    """
    Build module status table.

    Args:
        modules:
            Executed module names.

    Returns:
        HTML module status table.
    """

    rows = []

    for module in sorted(modules):

        rows.append(f"""
<tr>

<td>

{module.replace("_", " ").title()}

</td>

<td class="status-success">

✓ Completed

</td>

</tr>
""")

    return f"""
<div class="section">

<h2>

Module Status

</h2>

<table>

<thead>

<tr>

<th style="width:75%;">

Module

</th>

<th>

Status

</th>

</tr>

</thead>

<tbody>

{''.join(rows)}

</tbody>

</table>

</div>
"""


# ==========================================================
# Build Findings Breakdown
# ==========================================================


def _build_findings_breakdown(
    analysis: dict,
) -> str:
    """
    Build findings breakdown table.

    Args:
        analysis:
            Dashboard analysis results.

    Returns:
        HTML findings table.
    """

    statistics = analysis["statistics"]

    results = analysis["results"]

    findings = {
        "Subdomains": len(
            results.get(
                "subdomains",
                [],
            )
        ),
        "Alive Hosts": len(
            results.get(
                "alive_hosts",
                [],
            )
        ),
        "Open Ports": len(
            results.get(
                "ports",
                [],
            )
        ),
        "URLs": len(
            results.get(
                "urls",
                [],
            )
        ),
        "JavaScript Files": len(
            results.get(
                "javascript",
                [],
            )
        ),
        "Technologies": len(
            results.get(
                "technologies",
                [],
            )
        ),
        "Screenshots": len(
            results.get(
                "screenshots",
                [],
            )
        ),
    }

    rows = []

    for category, count in findings.items():

        rows.append(f"""
<tr>

<td>

{category}

</td>

<td>

{count}

</td>

</tr>
""")

    rows.append(f"""
<tr>

<td>

<strong>Total Findings</strong>

</td>

<td>

<strong>

{statistics["findings"]}

</strong>

</td>

</tr>
""")

    return f"""
<div class="section">

<h2>

Findings Breakdown

</h2>

<table>

<thead>

<tr>

<th style="width:75%;">

Category

</th>

<th>

Count

</th>

</tr>

</thead>

<tbody>

{''.join(rows)}

</tbody>

</table>

</div>
"""


# ==========================================================
# Build Results Overview
# ==========================================================


def _build_results_overview(
    statistics: dict,
) -> str:
    """
    Build results overview section.

    Args:
        statistics:
            Dashboard statistics.

    Returns:
        HTML overview cards.
    """

    total_modules = max(
        statistics["modules"],
        1,
    )

    completed = statistics["completed_modules"]

    failed = statistics["failed_modules"]

    success_rate = round(
        (completed / total_modules) * 100,
        1,
    )

    failure_rate = round(
        (failed / total_modules) * 100,
        1,
    )

    if failed == 0:

        framework_status = "Healthy"

        framework_class = "status-success"

        framework_message = "All modules completed successfully."

    elif failed <= 2:

        framework_status = "Warning"

        framework_class = "status-warning"

        framework_message = "Some modules reported errors."

    else:

        framework_status = "Failed"

        framework_class = "status-failed"

        framework_message = "Multiple modules failed during execution."

    return f"""
<div class="section">

<h2>

Results Overview

</h2>

<div class="grid">

<div class="card">

<h3>

Success Rate

</h3>

<h2 class="status-success">

{success_rate}%

</h2>

<div class="progress">

<div

class="progress-bar-success"

style="width:{success_rate}%">

</div>

</div>

</div>


<div class="card">

<h3>

Failure Rate

</h3>

<h2 class="status-failed">

{failure_rate}%

</h2>

<div class="progress">

<div

class="progress-bar-danger"

style="width:{failure_rate}%">

</div>

</div>

</div>


<div class="card">

<h3>

Framework Status

</h3>

<h2 class="{framework_class}">

{framework_status}

</h2>

<p
style="
margin-top:16px;
line-height:1.7;
color:#94a3b8;
">

{framework_message}

</p>

</div>

</div>

</div>
"""


# ==========================================================
# Build Framework Information
# ==========================================================


def _build_framework_information(
    analysis: dict,
) -> str:
    """
    Build framework information section.

    Args:
        analysis:
            Dashboard analysis.

    Returns:
        HTML framework information.
    """

    statistics = analysis["statistics"]

    framework = {
        "Framework": "Recon Automation Framework",
        "Version": "v1.0.0",
        "Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Target": statistics["target"],
        "Modules": statistics["modules"],
        "Completed": statistics["completed_modules"],
        "Failed": statistics["failed_modules"],
        "Findings": statistics["findings"],
        "Output": str(DASHBOARD_DIR),
    }

    rows = []

    for key, value in framework.items():

        rows.append(f"""
<tr>

<td>

<strong>

{key}

</strong>

</td>

<td>

{value}

</td>

</tr>
""")

    return f"""
<div class="section">

<h2>

Framework Information

</h2>

<table>

<thead>

<tr>

<th style="width:35%;">

Property

</th>

<th>

Value

</th>

</tr>

</thead>

<tbody>

{''.join(rows)}

</tbody>

</table>

</div>
"""


# ==========================================================
# Build Footer
# ==========================================================


def _build_footer() -> str:
    """
    Build dashboard footer.

    Returns:
        HTML footer.
    """

    return f"""
<footer>

<hr>

<div
style="
display:flex;
justify-content:space-between;
align-items:center;
flex-wrap:wrap;
gap:20px;
padding:20px 0;
">

<div>

<h3>

Recon Automation Framework

</h3>

<p
style="
margin-top:8px;
color:#94a3b8;
">

Professional Modular Reconnaissance Framework

</p>

</div>

<div
style="
text-align:right;
color:#94a3b8;
">

<p>

Dashboard Version

<strong>

v1.0.0

</strong>

</p>

<p>

Generated

<strong>

{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

</strong>

</p>

</div>

</div>

<hr>

<p
style="
margin-top:18px;
text-align:center;
font-size:14px;
color:#64748b;
">

Generated automatically by
<strong>

Recon Automation Framework

</strong>

</p>

</footer>

</div>

</body>

</html>
"""


# ==========================================================
# Export HTML Dashboard
# ==========================================================


def export_html(
    analysis: dict,
) -> Path:
    """
    Export HTML dashboard.

    Args:
        analysis:
            Dashboard analysis.

    Returns:
        HTML file path.
    """

    create_output_directory()

    statistics = analysis["statistics"]

    results = analysis["results"]

    modules = results.get(
        "module_names",
        [],
    )

    css = _build_css()

    header = _build_header(
        statistics,
    )

    summary_cards = _build_summary_cards(
        statistics,
    )

    execution_summary = _build_execution_summary(
        statistics,
    )

    module_status = _build_module_status(
        modules,
    )

    findings_breakdown = _build_findings_breakdown(
        analysis,
    )

    results_overview = _build_results_overview(
        statistics,
    )

    framework_information = _build_framework_information(
        analysis,
    )

    footer = _build_footer()

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta
name="viewport"
content="width=device-width, initial-scale=1.0"
>

<title>

Recon Automation Framework Dashboard

</title>

{css}

</head>

<body>

{header}

{summary_cards}

{execution_summary}

{module_status}

{findings_breakdown}

{results_overview}

{framework_information}

{footer}

</body>

</html>
"""

    return write_html(
        DASHBOARD_HTML,
        html,
    )


# ==========================================================
# Show Summary
# ==========================================================


def show_summary(
    analysis: dict,
) -> None:
    """
    Display dashboard summary.
    """

    statistics = analysis["statistics"]

    print()

    print("=" * 80)

    print("Dashboard Summary")

    print("=" * 80)

    print(f"{'Target':<25}" f"{statistics['target']}")

    print(f"{'Modules':<25}" f"{statistics['modules']}")

    print(f"{'Completed':<25}" f"{statistics['completed_modules']}")

    print(f"{'Failed':<25}" f"{statistics['failed_modules']}")

    print(f"{'Findings':<25}" f"{statistics['findings']}")

    print("=" * 80)


# ==========================================================
# Export All
# ==========================================================


def export_all(
    analysis: dict,
) -> dict:
    """
    Export every dashboard report.

    Returns:
        Exported files.
    """

    create_output_directory()

    exported = {
        "txt": export_txt(analysis),
        "json": export_json(analysis),
        "summary": export_summary(analysis),
        "html": export_html(analysis),
    }

    success("Dashboard reports exported successfully.")

    return exported


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "export_json",
    "export_txt",
    "export_summary",
    "export_html",
    "export_all",
    "show_summary",
]
