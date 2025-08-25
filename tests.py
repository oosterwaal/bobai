from functions.run_python import run_python_file

def run_tests():
    print('run_python_file("calculator", "main.py"):\n')
    print(run_python_file("calculator", "main.py"))
    print()
    print('run_python_file("calculator", "main.py", ["3 + 5"]):\n')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print()
    print('run_python_file("calculator", "tests.py"):\n')
    print(run_python_file("calculator", "tests.py"))
    print()
    print('run_python_file("calculator", "../main.py"):\n')
    print(run_python_file("calculator", "../main.py"))
    print()
    print('run_python_file("calculator", "nonexistent.py"):\n')
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    run_tests()

