from comptests import comptest, run_module_tests


@comptest
def t1():
    return


if __name__ == "__main__":
    run_module_tests()
