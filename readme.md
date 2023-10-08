# requirements

* `.env` file with `PREFECT_API_URL` and `PREFECT_API_KEY`
* Docker (serverless package)
* AWS account (serverless deploy)
* create "s3/cache" block in prefect

# run

* npm install
* npm run deploy
* npm run invoke

# concerns

- a lambda crashed while running a flow, in prefect UI the flow is stuck in `Running` state
  - this causes some graphs to become unusable as the stuck flow reports long run times (currently "2d")

- `task_input_hash` uses `fn.__code__.co_code.hex()` - but this value stays the same if only updating constants within the function, expected cache busting does not occur

- the task run page has a few bugs
  - displays task inputs as `{"id":[]}` when it should be `{"id":"abc"}`
  - it shows Cache Key as "None", despite having provided `cache_key_fn=task_input_hash`
  - https://app.prefect.cloud/account/:acc_uuid/workspace/:ws_uuid/task-runs/task-run/:id
    - also fails to provide deep-link to "Task inputs" tab

- prefect adds significant overhead when creating flow/task runs, or transitioning states
  - in cache miss scenarios this might be ok, we can show a spinner to the user
  - but a cache hit would perform better if read directly from cache storage

- historical view of task output, for debugging purposes
  - the prefect UI doesn't seem to be a good place for doing this type of data browsing
      - an artifact per ID would need to be created, and the prefect UI does not work well with a high number of artifact IDs
  - may need to customize the ResultStorage to write the result to an append-only table

- unable to integrate deployments with serverless aws lambda
  - limited support for serverless run infra (gcp cloud run, azure ci, aws ecs only)
  - therefore, the "run deployment" parts of the UI are not usable for executing flows in lambda
  - requires flows to be manually invoked from elsewhere, e.g bespoke admin page

# todo

- [x] external s3 caching
- [x] concurrency=1 for dynamic ID tags
- [x] view history of compute for an ID tag via artifact
- [x] explore ui filtering on ID tags
- [x] update `get_meaning_task` source code, must re-compute on next request
- [x] add multiple steps (a, b, c)
- [x] allocate concurrency on task e.g `id=x/task-a`
- [x] lambda parameters - skip flag, execute single step, etc.
- [ ] accessing a value between runs, e.g. providing continuity to a chatgpt context, diff results
- [ ] reduce cold boot times (precompile to pyc?)
- [ ] benchmark with prefect vs without
