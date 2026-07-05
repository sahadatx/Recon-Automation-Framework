from modules.passive.helpers import execute_source


def run_subfinder(domain):

    command = [
        "subfinder",
        "-silent",
        "-d",
        domain,
    ]

    return execute_source(
        "Subfinder",
        command
    )