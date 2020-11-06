from srpn_calculator import SRPNCalculator
import sys


def main() -> None:
    calc = SRPNCalculator(max_stack_size=23)
    try:
        while True:
            calc(input())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
