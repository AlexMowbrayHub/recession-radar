from pathlib import Path
import re


# ============================================================
# FILE TYPES TO INSPECT
# ============================================================

extensions = {
    ".py",
    ".md",
    ".txt",
    ".csv",
    ".json",
    ".yml",
    ".yaml",
}


# ============================================================
# SUSPICIOUS PATTERNS
# ============================================================

patterns = {
    "possible hard-coded FRED API key":
        re.compile(
            r'fred_api_key\s*=\s*["\'][^"\']+["\']',
            re.IGNORECASE
        ),

    "PowerShell API assignment":
        re.compile(
            r'\$env:FRED_API_KEY\s*=\s*["\'][^"\']+["\']',
            re.IGNORECASE
        ),

    "generic API key assignment":
        re.compile(
            r'api[_-]?key\s*=\s*["\'][A-Za-z0-9_\-]{16,}["\']',
            re.IGNORECASE
        ),
}


# ============================================================
# SCAN
# ============================================================

findings = []


for path in Path(".").rglob("*"):

    if not path.is_file():
        continue


    if path.suffix.lower() not in extensions:
        continue


    try:

        text = path.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    except Exception:

        continue


    for name, pattern in patterns.items():

        if pattern.search(text):

            findings.append(
                (
                    str(path),
                    name
                )
            )


# ============================================================
# RESULT
# ============================================================

print(
    "\nRECESSION RADAR — SECURITY SCAN"
)

print("=" * 85)


if findings:

    print(
        "\nPOTENTIAL SECRETS FOUND:"
    )

    print()


    for path, reason in findings:

        print(
            f"{path} — {reason}"
        )


    print()

    print(
        "DO NOT PUSH TO GITHUB YET."
    )


else:

    print(
        "No obvious hard-coded API secrets detected."
    )

    print()

    print(
        "SECURITY SCAN PASSED"
    )