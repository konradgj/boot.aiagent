import unittest
from functions.get_files_info import get_files_info, get_file_content


class FilesTest(unittest.TestCase):
    def test_dot(self):
        info = get_files_info("calculator", ".")
        # print(info)
        self.assertEqual(
            info,
            """- main.py: file_size=576 bytes, is_dir=False
- tests.py: file_size=1343 bytes, is_dir=False
- pkg: file_size=66 bytes, is_dir=True
- lorem.txt: file_size=67562 bytes, is_dir=False""",
        )

    def test_dir(self):
        info = get_files_info("calculator", "pkg")
        # print(info)
        self.assertEqual(
            info,
            """- calculator.py: file_size=1739 bytes, is_dir=False
- render.py: file_size=768 bytes, is_dir=False
- __pycache__: file_size=96 bytes, is_dir=True""",
        )

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

    def test_lorem(self):
        file = get_file_content("calculator", "lorem.txt")
        # print(file)
        self.assertTrue("truncated at 10000 characters]" in file)

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


if __name__ == "__main__":
    unittest.main()
