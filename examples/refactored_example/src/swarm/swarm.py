import json
from openai import OpenAI
from src.tasks.task import Task,EvaluationTask
from src.swarm.engines.assistants_engine import AssistantsEngine
from src.swarm.engines.local_engine import LocalEngine
from src.utils import Colors

class Swarm:
    def __init__(self,swarm, settings, engine_name, tasks=[], persist=False):
        self.swarm = swarm
        self.settings = settings
        self.tasks = tasks
        self.engine_name = engine_name
        self.engine = None
        self.persist = persist


    def deploy(self, test_mode=False, test_file_paths=None):
        """
        Processes all tasks in the order they are listed in self.tasks.
        """
        client = OpenAI()
        #Initialize swarm first
        if self.engine_name == 'assistants':
            print(f"{Colors.GREY}Selected engine: Assistants{Colors.ENDC}")
            self.engine = AssistantsEngine(client,self.tasks)
            self.engine.deploy(client,self.swarm,test_mode,test_file_paths)

        elif self.engine_name =='local':
            print(f"{Colors.GREY}Selected engine: Local{Colors.ENDC}")
            self.engine = LocalEngine(client, self.tasks, self.settings, persist=self.persist)
            self.engine.deploy(client, self.swarm, test_mode, test_file_paths)

    def load_tasks(self, tasks_path):
        self.tasks = []
        with open(tasks_path, 'r') as file:
            tasks_data = json.load(file)
            for task_json in tasks_data:
                task = Task(description=task_json['description'],
                            iterate=task_json.get('iterate', False),
                            evaluate=task_json.get('evaluate', False),
                            assistant=task_json.get('assistant', 'user_interface'))
                self.tasks.append(task)

    def add_task(self, task):
        self.tasks.append(task)
