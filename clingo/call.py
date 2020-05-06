import json
import random
import time
from subprocess import Popen, PIPE

from clingo.aspresult import Result

CLINGO_LOCATION = "clingo"

CLINGO_SOLUTION_SPLIT_TOKEN = " "

TIME_LIMIT_SOLVING = 10800
RANDOMIZATION = 0.01

RESTART_MODEL_AMOUNT = 1
SOUND_ON_DONE = False
PRINT_OUTPUT = False
PROJECT = False
CORES = 4

def call_clingo(file, optimization=True):
    # when optimizing model value of 0 denotes waiting as long as needed on the optimum, 1 is the correct value when any solution
    # acquiring the hard constraints will do.
    start = time.time()
    clingo_query = [CLINGO_LOCATION, file, "--verbose=0", # "" if optimization else "--opt-mode=ignore",
                    f"--parallel-mode={CORES}", #"--models=" + str(0) if optimization else str(1) + " opt-mode=ignore",
                    "--opt-mode=opt" if optimization else "--opt-mode=ignore",
                    "--configuration=auto"
                 , "--seed=" + str(random.randint(0, 2 ** 20)),  "--time-limit=" + str(TIME_LIMIT_SOLVING)
               ] + ([f"--rand-freq={RANDOMIZATION}"] if not optimization and RANDOMIZATION else []) + \
    ("--project=project" if PROJECT else [])
    print(" ".join(clingo_query))
    p = Popen(clingo_query, stdin=PIPE, stdout=PIPE)
    output = p.stdout.readlines()
    end = time.time()
    print("time taken by solver: " + str(end - start))
    print(len(output))
    # print(output)
    # if len(output) < 2:
    #     raise ValueError('Clingo instance was unsatisfiable')
    if PRINT_OUTPUT:
        print(output)
    solution = None
    for line in reversed(output):
        if b"assign" in line:
            solution = line
            break
    if solution is None:
        raise ValueError('Clingo instance was unsatisfiable')
    # solution = [output[-3]] + [output[-1]] if optimization else [output[-2]] + [output[-1]]
    # print(output)
    # solution = [output[-3]] + [output[-1]] if len(output) > 2 else [output[-2]] + [output[-1]]
    print("solution: " + str(solution))
    return Result({"Call": [{"Witnesses": [{"Value": solution.decode("utf-8").split(CLINGO_SOLUTION_SPLIT_TOKEN)}]}]})


def call_clingo_for_multiple(file, optimization=True, model_amount=0):
    clingo_query = ["clingo",
                    file,
                    "--outf=2",
                    f"--parallel-mode={CORES}",
                    "--models=" + str(model_amount),
                    "--seed=" + str(random.randint(0, 2 ** 20)),
                    "--time-limit=" + str(TIME_LIMIT_SOLVING)] +\
                   ([] if optimization else ["--opt-mode=ignore"]) +\
                                            ([f"--rand-freq={RANDOMIZATION}"] if not optimization and RANDOMIZATION else [])+ \
    ("--project=project" if PROJECT else [])
    print(" ".join(clingo_query))
    start = time.time()
    p = Popen(clingo_query, stdin=PIPE, stdout=PIPE)
    output = p.stdout.readlines()
    end = time.time()
    print("time taken by solver: " + str(end - start))
    if SOUND_ON_DONE:
        winsound.Beep(2500, 250)
    json_lines = []
    seen_start_of_json = False
    if PRINT_OUTPUT:
        print(output)
    for line in output:
        line = line.decode("utf-8")
        if not seen_start_of_json and line.startswith("{"):
            seen_start_of_json = True
        if seen_start_of_json:
            json_lines.append(line)
    solutions_object = json.loads("\n".join(json_lines))
    return Result(solutions_object)

def call_gringo_clasp_combination(file, optimization=False, model_amount=0):
    """
    In this subprocess first the grounded program is created with gringo and from that
    a number of models are found using clasp. In this way the models are very different.
    :param file:
    :param optimization:
    :param models:
    :return:
    """
    grounded_asp_file = "g.asp"
    with open(grounded_asp_file, "wb") as out, open("stderr.txt", "wb") as err:
        gringo_query = ["gringo",
                        file]
        Popen(gringo_query, stdin=out, stdout=err)

    def clingo_query(seed):
        return ["clingo",
         file,
         "--outf=2",
         f"--parallel-mode={CORES}",
         "--models=" + str(RESTART_MODEL_AMOUNT),
         "--seed=" + str(seed),
         "--time-limit=" + str(TIME_LIMIT_SOLVING)] + \
        ([] if optimization else ["--opt-mode=ignore"]) + \
        ([f"--rand-freq={RANDOMIZATION}"] if not optimization and RANDOMIZATION else [])+ \
    ("--project=project" if PROJECT else [])

    # p = Popen(clingo_query, stdin=PIPE, stdout=PIPE)
    # output = p.stdout.readlines()
    # agg_result = get_result(output)
    for i in range(0, model_amount if model_amount else 1):
        clingo_query_l = clingo_query(random.randint(0, 2 ** 20))
        print(" ".join(clingo_query_l))
        start = time.time()
        p = Popen(clingo_query_l, stdin=PIPE, stdout=PIPE)

        output = p.stdout.readlines()
        if PRINT_OUTPUT:
            print(output)
        result = get_result(output)
        # agg_result.merge(result)
        if SOUND_ON_DONE:
            import winsound
            winsound.Beep(2500, 250)
        # if yielding:
        #     agg_result = result
        end = time.time()
        print("time taken by solver: " + str(end - start))
        yield result
    # if not yielding:
    #     return agg_result



def get_result(output):
    json_lines = []
    seen_start_of_json = False
    for line in output:
        line = line.decode("utf-8")
        if not seen_start_of_json and line.startswith("{"):
            seen_start_of_json = True
        if seen_start_of_json:
            json_lines.append(line)
    solutions_object = json.loads("\n".join(json_lines))
    return Result(solutions_object)
