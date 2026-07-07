"""
HTML Parser

Extracts useful information from HTML pages.
"""

import re

from bs4 import BeautifulSoup

from modules.crawler.helpers import (
    normalize_url,
    same_domain,
)


# ==========================================================
# Extract Links
# ==========================================================

def extract_links(
    base_url: str,
    soup: BeautifulSoup,
):
    """
    Extract internal and external links.

    Returns:
        tuple[list, list]
    """

    internal = set()
    external = set()

    for tag in soup.find_all(
        "a",
        href=True,
    ):

        href = tag["href"].strip()

        if (
            not href
            or href.startswith("#")
            or href.startswith("javascript:")
            or href.startswith("mailto:")
            or href.startswith("tel:")
        ):
            continue

        url = normalize_url(
            base_url,
            href,
        )

        if same_domain(
            base_url,
            url,
        ):
            internal.add(url)

        else:
            external.add(url)

    return (
        sorted(internal),
        sorted(external),
    )


# ==========================================================
# Extract JavaScript Files
# ==========================================================

def extract_scripts(
    base_url: str,
    soup: BeautifulSoup,
):
    """
    Extract JavaScript files.

    Returns:
        list
    """

    scripts = set()

    for script in soup.find_all(
        "script",
        src=True,
    ):

        scripts.add(
            normalize_url(
                base_url,
                script["src"],
            )
        )

    return sorted(scripts)


# ==========================================================
# Extract CSS Assets
# ==========================================================

def extract_css(
    base_url: str,
    soup: BeautifulSoup,
):
    """
    Extract CSS files.

    Returns:
        list
    """

    css = set()

    for tag in soup.find_all(
        "link",
        href=True,
    ):

        rel = tag.get(
            "rel",
            [],
        )

        rel = [
            r.lower()
            for r in rel
        ]

        if "stylesheet" in rel:

            css.add(
                normalize_url(
                    base_url,
                    tag["href"],
                )
            )

    return sorted(css)


# ==========================================================
# Extract Forms
# ==========================================================

def extract_forms(
    base_url: str,
    soup: BeautifulSoup,
):
    """
    Extract HTML forms.

    Returns:
        list
    """

    forms = []

    for form in soup.find_all(
        "form"
    ):

        forms.append(
            {

                "method": form.get(
                    "method",
                    "GET",
                ).upper(),

                "action": normalize_url(
                    base_url,
                    form.get(
                        "action",
                        "",
                    ),
                ),

            }
        )

    return forms


# ==========================================================
# Extract Meta Refresh
# ==========================================================

def extract_meta_refresh(
    soup: BeautifulSoup,
):
    """
    Extract meta refresh URL.

    Returns:
        str | None
    """

    meta = soup.find(
        "meta",
        attrs={
            "http-equiv": (
                lambda x:
                x
                and
                x.lower() == "refresh"
            )
        },
    )

    if not meta:

        return None

    content = meta.get(
        "content",
        "",
    )

    match = re.search(
        r"url=(.*)",
        content,
        re.I,
    )

    if match:

        return match.group(
            1
        ).strip()

    return None


# ==========================================================
# Extract Emails
# ==========================================================

def extract_emails(
    html: str,
):
    """
    Extract email addresses.

    Returns:
        list
    """

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    return sorted(
        set(
            re.findall(
                pattern,
                html,
            )
        )
    )


# ==========================================================
# Parse HTML
# ==========================================================

def parse_html(
    url: str,
    html: str,
):
    """
    Parse HTML page.

    Returns:
        dict
    """

    soup = BeautifulSoup(
        html,
        "lxml",
    )

    internal, external = extract_links(
        url,
        soup,
    )

    javascript = extract_scripts(
        url,
        soup,
    )

    css = extract_css(
        url,
        soup,
    )

    forms = extract_forms(
        url,
        soup,
    )

    meta_refresh = extract_meta_refresh(
        soup,
    )

    emails = extract_emails(
        html,
    )


    return {

        "internal_links": internal,

        "external_links": external,

        "javascript": javascript,

        "css": css,

        "forms": forms,

        "meta_refresh": meta_refresh,

        "emails": emails,

        "statistics": {

            "internal_links": len(
                internal
            ),

            "external_links": len(
                external
            ),

            "javascript": len(
                javascript
            ),

            "css": len(
                css
            ),

            "forms": len(
                forms
            ),

            "emails": len(
                emails
            ),

        },

    }