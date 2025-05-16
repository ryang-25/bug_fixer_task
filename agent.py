# what kind of ai agent?
# tree of thoughts
# localization a la tree-sitter ast / locagent
# agentless or codeact? https://arxiv.org/pdf/2503.14269
# https://arxiv.org/pdf/2410.20285
# https://arxiv.org/pdf/2407.01489
# https://github.com/kodu-ai/claude-coder/tree/main/extension/src

# I would like to create an AI agent python code localization agent

from datasets import load_dataset
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent, SequentialAgent

from parser import parse_codebase

import os
import subprocess
import time

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
APP_NAME = "bug_fixer"
MODEL_NAME = "gemini-2.5-flash-preview"

# def init_dataset():
  # Login using e.g. `huggingface-cli login` to access this dataset


def set_repo(repo_name, commit_id, base_path):
  url = "https://github.com/" + repo_name + ".git"
  _, name = url.split("/")
  path = os.path.join(base_path, name)

  if os.path.exists(path):
      # Repository already exists, reset any changes and fetch only what's needed
      repo = Repo(path)
      repo.git.reset("--hard")
      repo.git.clean("-fdx")  # Remove untracked files
      # Only fetch the specific commit
      repo.git.fetch("origin", commit_id, depth=1)
      repo.git.checkout(commit_id)
  else:
      repo = Repo.clone_from(
          url, 
          path, 
          depth=1,
          no_checkout=True,
          filter="blob:none",
          single_branch=True
      )
      # Only fetch the specific commit
      repo.git.fetch("origin", commit_id, depth=1)
      repo.git.checkout(commit_id)
  return path



def fetch_repo_commit(repo_name, commit_id, base_path):
  pass


def bench():
  # G = parse_codebase("")

  # # Should be cached
  # dataset = load_dataset("princeton-nlp/SWE-bench_Lite", streaming=True, split="test")
  # for entry in dataset:
  #   repo = entry["repo"]
  #   instance_id = entry["instance_id"]
  #   problem_statement = entry["problem_statement"]
  #   commit_id = entry["environment_setup_commit"]
  pass


def communicate_shell():
  pass

def main():
  sh = subprocess.Popen("/bin/sh", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  ipy = subprocess.Popen("/bin/i", stdin=subprocess.PIPE, stdout=subprocess.PIPE)

  def comm_ipython():
    pass
  def comm_shell():
    pass

  agent = LlmAgent(
    model=MODEL_NAME,
    name="SpawnAgent",
    description="Shell spawning agent",
    instruction=f"""
    You are an advanced bug fixing AI agent
    """
    )

  root_agent = SequentialAgent(
    name="Bug fixing pipeline"
    )

  agent = LlmAgent(
      model=MODEL_NAME
      name=APP_NAME,
      description="An agentic bug fixer",
      instruction=f"""
      You are an advanced bug fixing AI agent that, given a bug report, feature
      request, or other natural language description, can solve it effortlessly
      on a user's behalf.

      Your current working directory is {cwd}. The user will provide you with a
      description of their problem and the path on the filesystem on which a copy
      of the repository may be located.
      """
      tools=[spawn_shell, communicate_shell]
    )
  service = InMemorySessionService()
  session = service.create_session(
    app_name=APP_NAME, 
    user_id="user0", 
    session_id="session0"
  )
  runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=service
  )

  # I guess os.chdir will work in this case

  # parse_file(open("test.py", "rb"))


# def main():
  agent = LlmAgent(
      model=MODEL_NAME
      name=APP_NAME,
      description="Fixes single line bugs.",
      instruction="""
      """
    )
  service = InMemorySessionService()
  session = service.create_session(
    app_name=APP_NAME, 
    user_id="user0", 
    session_id="session0"
  )
  runner = Runner(
    agent=agent,
    app_name=APP_NAME,
    session_service=service
  )

if __name__ == '__main__':
  main()