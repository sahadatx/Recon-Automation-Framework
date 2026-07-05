from core.banner import show_banner
from modules.passive.crtsh import run_crtsh


def main():

    show_banner()

    results = run_crtsh("example.com")

    print()

    for subdomain in results:

        print(subdomain)

    print()

    print(f"Total: {len(results)}")


if __name__ == "__main__":
    main()