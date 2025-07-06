import unittest
from functions.file_helpers import get_files_info, get_file_content, write_file
from functions.run_python import run_python_file


class FilesTest(unittest.TestCase):
    def test_dot(self):
        info = get_files_info("calculator", ".")
        # print(info)
        self.assertTrue("""- main.py:""" in info)

    def test_dir(self):
        info = get_files_info("calculator", "pkg")
        # print(info)
        self.assertTrue("- calculator.py: " in info)

    def test_slash(self):
        info = get_files_info("calculator", "/bin")
        # print(info)
        self.assertEqual(
            info,
            """Error: Cannot list '/bin' as it is outside the permitted working directory""",
        )

    def test_dotdot(self):
        info = get_files_info("calculator", "../")
        # print(info)
        self.assertEqual(
            info,
            """Error: Cannot list '../' as it is outside the permitted working directory""",
        )

    def test_word(self):
        info = get_files_info("calculator", "main.py")
        self.assertEqual(
            info,
            """Error: 'main.py' is not a directory""",
        )

    def test_main(self):
        file = get_file_content("calculator", "main.py")
        # print(file)
        self.assertTrue("def main():" in file)

    def test_calc(self):
        file = get_file_content("calculator", "pkg/calculator.py")
        # print(file)
        self.assertTrue("def _apply_operator(self, operators, values)" in file)

    def test_bincat(self):
        file = get_file_content("calculator", "/bin/cat")
        # print(file)
        self.assertEqual(
            file,
            "Error: Cannot read '/bin/cat' as it is outside the permitted working directory",
        )

    def test_wlorem(self):
        res = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        print(res)
        self.assertTrue("Successfully wrote to " in res)

    def test_mlorem(self):
        res = write_file(
            "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
        )
        print(res)
        self.assertTrue("Successfully wrote to " in res)

    def test_tmp(self):
        res = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(res)
        self.assertTrue("Error: Cannot write to" in res)

    def test_rmain(self):
        res = run_python_file("calculator", "main.py")
        print(res)
        self.assertTrue("Calculator App\nUsage: python main.py" in res)

    def test_rtest(self):
        res = run_python_file("calculator", "tests.py")
        print(res)
        self.assertTrue(".......")

    def test_rout(self):
        res = run_python_file("calculator", "../main.py")
        print(res)
        self.assertTrue("Error: Cannot execute" in res)

    def test_rnofile(self):
        res = run_python_file("calculator", "nonexistent.py")
        print(res)
        self.assertTrue("Error: File " in res)


if __name__ == "__main__":
    unittest.main()
