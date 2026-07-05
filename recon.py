from core.banner import show_banner
from modules.passive.subfinder import run_subfinder


def main():

    show_banner()

    results = run_subfinder("example.com")

    print()

    for subdomain in results:
        print(subdomain)

    print(f"\nTotal: {len(results)}")


if __name__ == "__main__":
    main()