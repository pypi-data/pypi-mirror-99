import argparse


def main():
    args = _init_args()
    _print_args(args)


def _init_args():
    p = argparse.ArgumentParser()
    p.add_argument("--foo", default=1, help="Foo")
    p.add_argument("--bar", default=0.001, help="Bar")
    p.add_argument("--list", nargs="*", default=[])
    return p.parse_args()


def _print_args(args):
    print("bar: {}".format(args.bar))
    print("foo: {}".format(args.foo))


if __name__ == "__main__":
    main()
