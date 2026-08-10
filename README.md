# Orchestration

Orchestration tools, workflows, and automation for managing multi-service systems.

## Orchestration Layer

The orchestration layer is what turns independent agents and services into a coordinated system. Instead of letting each component act on its own, the orchestration layer directs how work flows from start to finish. It covers:

- **Agent workflow management**: Define and manage the steps each agent follows, and how work is routed between agents and services.
- **Multi-step planning and execution**: Break complex goals into ordered steps, then execute them while keeping track of progress and dependencies.
- **Error handling and recovery**: Detect failures mid-workflow, retry or reroute steps, and recover gracefully without losing the overall state of the task.
- **Parallel vs. sequential execution**: Choose when steps can run in parallel (independent work) versus sequentially (dependent work), to maximize speed while preserving correctness.
- **Agent-to-agent communication**: Enable agents to talk to each other, hand off tasks, and coordinate within multi-agent systems.

## Repositories

This repository aggregates several sub-projects using `git subtree`. Each sub-project lives in its own folder and retains its full git history:

| Folder |
| --- |
| `SDK/` |
| `Langchain-Labs/` |

## Extracting a sub-repository back into its own repo

Each folder is an independent git subtree, so you can extract any of them back into a standalone repository with its complete commit history.

### Example: extract `SDK`

```bash
# 1. Split the SDK folder's history into a temporary branch
git subtree split --prefix=SDK -b sdk-back

# 2. Create a new standalone repo
mkdir SDK-standalone && cd SDK-standalone
git init

# 3. Fetch the extracted history from the Orchestration repo
git remote add orchestration /path/to/orchestration
git fetch orchestration sdk-back

# 4. Check out the history as the new repo's default branch
git checkout -b main FETCH_HEAD

# 5. Push to its new remote
git remote add origin https://github.com/<your-org>/SDK.git
git push -u origin main
```

### Extracting any other folder

The same command works for any folder. Just change the folder name in **two places**:

```bash
git subtree split --prefix=<FOLDER-NAME> -b <folder-name>-back
```

1. `--prefix=<FOLDER-NAME>` — the exact folder name in this repo, e.g. `--prefix=Langchain-Labs`.
2. `-b <folder-name>-back` — the temporary branch name, e.g. `-b langchain-labs-back`.

Then follow steps 2–5 above, replacing the branch name in step 3 and the target URL in step 5.

## License

[MIT](LICENSE)
