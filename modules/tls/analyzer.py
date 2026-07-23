"""
TLS Security Analyzer

Analyze certificate,
protocol and cipher
security.
"""

from __future__ import annotations

from copy import deepcopy


# ==========================================================
# Default Analysis
# ==========================================================

EMPTY_ANALYSIS = {

    "expired": False,

    "self_signed": False,

    "hostname_match": False,

    "wildcard": False,

    "days_remaining": 0,

    "weak_protocol": False,

    "weak_cipher": False,

    "forward_secrecy": False,

    "risk_score": 0,

    "risk_level": "Safe",

    "recommendations": [],

}


# ==========================================================
# Risk Levels
# ==========================================================

RISK_LEVELS = (

    (90, "Critical"),

    (70, "High"),

    (40, "Medium"),

    (20, "Low"),

    (0, "Safe"),

)


# ==========================================================
# Recommendation Database
# ==========================================================

RECOMMENDATIONS = {

    "expired":

        "Replace the expired certificate immediately.",

    "self_signed":

        "Use a trusted Certificate Authority.",

    "hostname":

        "Certificate hostname does not match the target.",

    "wildcard":

        "Review wildcard certificate usage.",

    "weak_protocol":

        "Disable legacy TLS versions.",

    "weak_cipher":

        "Replace weak cipher suites.",

    "forward_secrecy":

        "Enable Forward Secrecy (ECDHE/DHE).",

}


# ==========================================================
# Risk Level
# ==========================================================

def calculate_risk_level(
    score: int,
):
    """
    Convert risk score
    to human readable
    level.
    """

    for minimum, level in RISK_LEVELS:

        if score >= minimum:

            return level

    return "Unknown"


# ==========================================================
# Weak Protocol
# ==========================================================

def is_weak_protocol(
    protocol: str,
):
    """
    Check protocol security.
    """

    return protocol in (

        "SSLv2",

        "SSLv3",

        "TLSv1",

        "TLSv1.1",

        "TLS 1.0",

        "TLS 1.1",

    )

# ==========================================================
# Risk Score
# ==========================================================

def calculate_risk_score(
    analysis: dict,
):
    """
    Calculate overall
    TLS security risk.

    Returns:
        int
    """

    score = 0

    if analysis["expired"]:

        score += 40

    if analysis["self_signed"]:

        score += 30

    if not analysis["hostname_match"]:

        score += 25

    if analysis["weak_protocol"]:

        score += 20

    if analysis["weak_cipher"]:

        score += 20

    if not analysis["forward_secrecy"]:

        score += 10

    if analysis["wildcard"]:

        score += 5

    return min(

        score,

        100,

    )


# ==========================================================
# Recommendations
# ==========================================================

def build_recommendations(
    analysis: dict,
):
    """
    Generate security
    recommendations.

    Returns:
        list[str]
    """

    recommendations = []

    if analysis["expired"]:

        recommendations.append(

            RECOMMENDATIONS["expired"],

        )

    if analysis["self_signed"]:

        recommendations.append(

            RECOMMENDATIONS["self_signed"],

        )

    if not analysis["hostname_match"]:

        recommendations.append(

            RECOMMENDATIONS["hostname"],

        )

    if analysis["wildcard"]:

        recommendations.append(

            RECOMMENDATIONS["wildcard"],

        )

    if analysis["weak_protocol"]:

        recommendations.append(

            RECOMMENDATIONS["weak_protocol"],

        )

    if analysis["weak_cipher"]:

        recommendations.append(

            RECOMMENDATIONS["weak_cipher"],

        )

    if not analysis["forward_secrecy"]:

        recommendations.append(

            RECOMMENDATIONS["forward_secrecy"],

        )

    return recommendations


# ==========================================================
# Certificate Analysis
# ==========================================================

def analyze_certificate(
    certificate: dict,
):
    """
    Analyze certificate
    summary.

    Returns:
        dict
    """

    return {

        "expired":

            certificate.get(

                "expired",

                False,

            ),

        "self_signed":

            certificate.get(

                "self_signed",

                False,

            ),

        "hostname_match":

            certificate.get(

                "hostname_match",

                False,

            ),

        "wildcard":

            certificate.get(

                "wildcard",

                False,

            ),

        "days_remaining":

            certificate.get(

                "days_remaining",

                0,

            ),

    }


# ==========================================================
# Protocol Analysis
# ==========================================================

def analyze_protocol(
    protocols: dict,
):
    """
    Analyze protocol
    summary.

    Returns:
        dict
    """

    protocol = protocols.get(

        "highest_protocol",

        "",

    )

    return {

        "weak_protocol":

            is_weak_protocol(

                protocol,

            ),

    }


# ==========================================================
# Cipher Analysis
# ==========================================================

def analyze_cipher(
    cipher: dict,
):
    """
    Analyze cipher
    summary.

    Returns:
        dict
    """

    return {

        "weak_cipher":

            cipher.get(

                "weak",

                False,

            ),

        "forward_secrecy":

            cipher.get(

                "forward_secrecy",

                False,

            ),

    }


# ==========================================================
# Analyze
# ==========================================================

def analyze(
    certificate: dict,
    protocols: dict,
    cipher: dict,
):
    """
    Analyze TLS security.

    Returns:
        dict
    """

    result = deepcopy(

        EMPTY_ANALYSIS,

    )

    result.update(

        analyze_certificate(

            certificate,

        )

    )

    result.update(

        analyze_protocol(

            protocols,

        )

    )

    result.update(

        analyze_cipher(

            cipher,

        )

    )

    result["risk_score"] = (

        calculate_risk_score(

            result,

        )

    )

    result["risk_level"] = (

        calculate_risk_level(

            result["risk_score"],

        )

    )

    result["recommendations"] = (

        build_recommendations(

            result,

        )

    )

    return result


# ==========================================================
# Summary
# ==========================================================

def analysis_summary(
    analysis: dict,
):
    """
    Create analysis summary.

    Returns:
        dict
    """

    if not analysis:

        return {}

    return {

        "risk_score":

            analysis.get(

                "risk_score",

                0,

            ),

        "risk_level":

            analysis.get(

                "risk_level",

                "Unknown",

            ),

        "expired":

            analysis.get(

                "expired",

                False,

            ),

        "self_signed":

            analysis.get(

                "self_signed",

                False,

            ),

        "hostname_match":

            analysis.get(

                "hostname_match",

                False,

            ),

        "wildcard":

            analysis.get(

                "wildcard",

                False,

            ),

        "days_remaining":

            analysis.get(

                "days_remaining",

                0,

            ),

        "weak_protocol":

            analysis.get(

                "weak_protocol",

                False,

            ),

        "weak_cipher":

            analysis.get(

                "weak_cipher",

                False,

            ),

        "forward_secrecy":

            analysis.get(

                "forward_secrecy",

                False,

            ),

        "recommendations":

            analysis.get(

                "recommendations",

                [],

            ),

    }


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "EMPTY_ANALYSIS",

    "calculate_risk_level",

    "calculate_risk_score",

    "build_recommendations",

    "is_weak_protocol",

    "analyze_certificate",

    "analyze_protocol",

    "analyze_cipher",

    "analyze",

    "analysis_summary",

]