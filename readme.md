# requirements

* Docker
* `.env` file with `PREFECT_API_URL` and `PREFECT_API_KEY`

# run

* npm install
* npm run deploy
* npm run invoke

# todo

- [x] external s3 caching
- [x] concurrency=1 for dynamic ID tags
- [x] view history of compute for an ID tag via artifact
- [x] explore ui filtering on ID tags
- [ ] update `get_meaning_task` source code, must re-compute on next request
      - 🛑 blocked: this didn't work, I updated the function source code and the Cached value was still returned
- [ ] add multiple sub-steps (a, b, c)
- [ ] allocate concurrency on sub-step e.g `id=x & step=a`
- [ ] lambda parameters - skip flag, execute single step, etc.
- [ ] accessing a value between runs, e.g. providing continuity to a chatgpt context
- [ ] reduce cold boot times (precompile to pyc?)

# concerns

- a lambda crashed while running a flow, the flow is still displayed as `Running` some 3 hours later

- prefect adds significant overhead when creating flow/task runs, or transitioning states
  - in cache miss scenarios this might be ok, we can show a spinner to the user
  - but a cache hit would perform better if read directly from cache storage

- historical view of task output, for debugging purposes
  - the prefect UI doesn't seem to be a good place for doing this type of data browsing
      - an artifact per ID would need to be created, and the prefect UI does not work well with a high number of artifact IDs
  - may need to customize the ResultStorage to write the result to an append-only table
