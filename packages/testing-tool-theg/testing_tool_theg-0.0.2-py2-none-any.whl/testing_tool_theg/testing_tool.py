passed = []


def checker():
    print("Usage:")
    print("\t- Check value : your_instance(exp, got)")
    print("\t- Get Results : your_instance(0,0,True)")

    passed = []

    class test:

        def __init__(self, exp, got, get_final=False):
            if not get_final:
                self.got = got
                self.exp = exp
                self.passing = (got == exp)

                self.check()
            else:
                self.passing = (not (False in passed))
                self.get_final_check()

        def __repr__(self):
            return ("[\x1b[32mPASS\x1b[0m]" if self.passing else "[\x1b[31mFAIL\x1b[0m]")

        def check(self):
            passed.append(self.passing)
            print(f"Test     : {len(passed):02d}")

            print("Expected : " + str(self.exp))
            print("got      : " + str(self.got))

        def get_final_check(self):
            for i in range(len(passed)):
                check = ("[\x1b[32mPASS\x1b[0m]" if passed[i]
                         else "[\x1b[31mFAIL\x1b[0m]")
                print(f'test {(i + 1):02d}: %s' % (check))
            print("\nSome tests have failed") if not self.passing else print(
                "\nYou're all clear")

    return test
