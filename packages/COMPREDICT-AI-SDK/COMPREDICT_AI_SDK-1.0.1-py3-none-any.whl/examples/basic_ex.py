from compredict.client import api
import compredict
from compredict.resources import resources
from compredict.resources import Task, Result
from time import sleep
from environs import Env
from sys import exit
import shutil
import json
import sys
import pandas as pd

env = Env()
env.read_env()

token = env("COMPREDICT_AI_CORE_KEY")
callback_url = env("COMPREDICT_AI_CORE_CALLBACK", None)
fail_on_error = env("COMPREDICT_AI_CORE_FAIL_ON_ERROR", False)
ppk = env("COMPREDICT_AI_CORE_PPK", None)
passphrase = env("COMPREDICT_AI_CORE_PASSPHRASE", "")

client = api.get_instance(token="ae575090b16038d68a246e0e6fca5a944e3a6c4d", callback_url=callback_url, ppk=ppk,
                          passphrase=passphrase, url="http://localhost:8800/api/v1")
client.fail_on_error(option=False)

algorithms = client.get_algorithms()

body_algorithm = client.get_algorithm("base-damage-forecaster")
#
# path = "test_small.parquet"
# df = pd.read_csv("test_observer.csv", index_col=None)
#
with open("base-damage-forecaster.json") as f:
    data = json.load(f)

# run = body_algorithm.run(df, file_content_type="application/parquet")
# print(run)

# run = body_algorithm.run("sample-big.parquet", file_content_type="application/parquet")
# if isinstance(run, compredict.resources.Task):
#     while run.get_current_status() != compredict.resources.Task.STATUS_FINISHED:
#         print("not finished, status is:", run.get_current_status(), ", retrying in 15 seconds...")
#         sleep(15)
#         run.update()
#
#     print("status: {}, success: {}".format(run.get_current_status(), run.success))
# get a graph
# algorithm = client.get_algorithm("auto-parameterization")
# graph = algorithm.get_detailed_graph()
# new_file = open('auto-parameterization-graph.png', 'wb')
# shutil.copyfileobj(graph, new_file)
# graph.close()

# with open("test_observer.json", "r") as f:
#     data_raw = f.read()
#     data = json.loads(data_raw)
#
# df = pd.DataFrame(data)
#
# algorithm = client.get_algorithm("observer")
# if algorithm is False:
#     print(client.last_error)
#     sys.exit()
# callback_param = dict(damage_id=5, damage_type=1)
# results = algorithm.run(df, evaluate=False, encrypt=False, callback_param=callback_param,
#                         file_content_type="application/json")

# algorithms = client.get_algorithms()
#
# # Check if the user has algorithms to predict
# if len(algorithms) == 0:
#     print("No algorithms to proceed!")
#     exit()
#
# algorithm = algorithms[0]
#
# tmp = algorithm.get_detailed_template()
# tmp.close()  # It is tmp file. close the file to remove it.
#
# data = dict()  # data for predictions
#
# results = algorithm.run(data, evaluate=False, encrypt=True)
#
# if results is False:
#     print("failed to predict with error", client.last_error)
# elif isinstance(results, resources.Task):
#     print(results.job_id)
#
#     while results.status != results.STATUS_FINISHED:
#         print("task is not done yet.. waiting...")
#         sleep(15)
#         results.update()
#
#     if results.success is True:
#         print(results.predictions)
#     else:
#         print(results.error)
# else:
#     print(results.results)


