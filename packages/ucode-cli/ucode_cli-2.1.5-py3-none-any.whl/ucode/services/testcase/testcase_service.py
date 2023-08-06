import json
import os
import time
from builtins import staticmethod
from itertools import product

from jinja2 import Template
from ucode.helpers.clog import CLog
from ucode.helpers.misc import dos2unix
from ucode.helpers.shell_helper import ShellHelper
from ucode.models.problem import Problem, TestCase


class TestcaseService:
    @staticmethod
    def execute(source_code_file: str, _input: str = "", raise_exception=True, timeout=60):
        """

        @param timeout:
        @param raise_exception:
        @param source_code_file:
        @param _input:
        @return: output, compile_time, execute_time
        """

        folder, file_name = os.path.split(source_code_file)
        file_base_name, file_ext = os.path.splitext(file_name)

        if file_ext == ".py":
            compile_needed = False
        else:
            compile_needed = True

        t0 = time.time()
        compile_time = -1

        owd = os.getcwd()
        os.chdir(folder)

        if compile_needed:
            if file_ext != ".cpp":
                CLog.error(f"Language not supported: `{file_ext}`")
                os.chdir(owd)
                return
            compile_cmd = ["C:\\Program Files\\CodeBlocks\\MinGW\\bin\\g++.exe", "-std=c++14",
                           file_name,
                           "-pipe", f"-o{file_base_name}.exe"]
            ShellHelper.execute(compile_cmd, timeout=timeout)
            compile_time = time.time() - t0

        if file_ext == ".py":
            run_cmd = ["python", file_name]
        else:
            run_cmd = [f"{file_base_name}.exe"]

        t0 = time.time()
        output = ShellHelper.execute(run_cmd, input=_input, raise_exception=raise_exception)
        execute_time = time.time() - t0
        os.chdir(owd)
        return output, compile_time, execute_time

    @staticmethod
    def save_testcases(problem_folder, problem: Problem, format="both"):
        """

        @param problem_folder:
        @param problem:
        @param format: ucode | themis | both
        @return:
        """
        template_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../dsa/templates')

        if format:
            if format == "ucode" or format == "both":
                CLog.info("Writing testcases in ucode format")
                testcases = problem.testcases
                if testcases:
                    with open(os.path.join(template_path, 'testcases.txt.j2'), encoding="utf-8") as file_:
                        template = Template(file_.read())
                        for i, t in enumerate(testcases):
                            t.name = "Test #%02d" % (i + 1)
                        content = template.render(testcases=testcases)
                        testcase_path = os.path.join(problem_folder, "testcases.txt")
                        f = open(testcase_path, 'w', encoding="utf-8", newline='')
                        f.write(dos2unix(content))
                        f.close()
                        CLog.info(f"Testcases saved to '{testcase_path}'")

                if problem.stock_testcases:
                    with open(os.path.join(template_path, 'testcases.txt.j2'), encoding="utf-8") as file_:
                        template = Template(file_.read())
                        for i, t in enumerate(problem.stock_testcases):
                            t.name = "Test #%02d" % (i + 1)
                        content = template.render(testcases=problem.stock_testcases)
                        testcase_path = os.path.join(problem_folder, "testcases_stock.txt")
                        f = open(testcase_path, 'w', encoding="utf-8", newline='')
                        f.write(dos2unix(content))
                        f.close()
                        CLog.info(f"Testcases saved to '{testcase_path}'")

                if problem.testcases_sample:
                    with open(os.path.join(template_path, 'testcases.txt.j2'), encoding="utf-8") as file_:
                        template = Template(file_.read())
                        for i, t in enumerate(problem.testcases_sample):
                            t.name = "Test #%02d" % (i + 1)
                        content = template.render(testcases=problem.testcases_sample)
                        testcase_path = os.path.join(problem_folder, "testcases_sample.txt")
                        f = open(testcase_path, 'w', encoding="utf-8", newline='')
                        f.write(dos2unix(content))
                        f.close()

    @staticmethod
    def generate_testcases(problem_folder, testcase_count=20,
                           programming_language=None, format=None, overwrite=False):
        """

        @param problem_folder:
        @param testcase_count:
        @param programming_language: py | cpp | pas, None = auto detect
        @param format: ucode | themis | both | None, None --> not save to disk
        @return:
        """
        from ucode.services.dsa.problem_service import ProblemService
        # problem: Problem = ProblemService.load(problem_folder)
        meta, folders = ProblemService.detect_problem_code_in_folder(problem_folder)
        # print(problem)
        print(json.dumps(folders))
        print(json.dumps(folders['solutions']))
        print(json.dumps(folders['test_generators']))
        # return
        input_generator_files = folders['test_generators']
        solution_files = folders['solutions']

        if not input_generator_files:
            CLog.error("No input generator file found!")
            return
        if not solution_files:
            CLog.error("No solution file found!")
            return

        input_generator_file = input_generator_files[0]
        solution_file = solution_files[0]
        if programming_language:
            prefered_generators = [v for v in input_generator_files if v.endswith(programming_language)]
            if prefered_generators:
                input_generator_file = prefered_generators[0]
            else:
                CLog.warn(f"No input generator file found for preferred language `{programming_language}`,"
                          f"Using `{input_generator_file}` instead.")

            prefered_solutions = [v for v in solution_files if v.endswith(programming_language)]
            if prefered_solutions:
                solution_file = prefered_solutions[0]
            else:
                CLog.warn(f"No solution file found for preferred language `{programming_language}`,"
                          f"Using `{input_generator_file}` instead.")

        input_generator_file = os.path.abspath(input_generator_file)
        solution_file = os.path.abspath(solution_file)
        print(input_generator_file, solution_file, sep='\n')

        testcases = []
        for i in range(1, testcase_count + 1):
            _input, input_compile_time, input_time = TestcaseService.execute(input_generator_file, _input=str(i),
                                                                             timeout=180)
            # print("input:", _input)
            _output, compile_time, output_time = TestcaseService.execute(solution_file, _input=_input.strip())

            testcases.append(TestCase(input=_input, output=_output))
            print("Testcase #%02d generated! Input generation compile time: %.2fs, "
                  "input generation running time: %.2fs, solution complie time: %.2f, solution running time: %.2fs"
                  % (i, input_compile_time, input_time, compile_time, output_time))

        if format:
            problem = Problem()
            problem.testcases = testcases
            TestcaseService.save_testcases(problem_folder, problem, format)
        return testcases


if __name__ == "__main__":
    folder = "D:\\projects\\ucode\\dsa-thematic-problems\\de_thi_hsg\\hanoi_2020_2021_thcs\\p4_itable"
    # folder = "../../../problems/p4_itable"
    T = TestcaseService.generate_testcases(problem_folder=folder, format="ucode",
                                           programming_language="cpp",
                                           testcase_count=10)
    print("testcases:", len(T))

