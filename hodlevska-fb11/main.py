import interpr

def get_line():
    l = input("> ")

    yield l
    while not (";" in l):
        l = input("... ")
        yield l


def main():
    parser = interpr.Parser()

    while True:
        q = ""
        for l in get_line():
            q += l

        try:
            parser.recvQuerry(q)
            parser.exec()
        except Exception as e:
            print(f"Exception: {e}")


if __name__ == "__main__":
    main()
