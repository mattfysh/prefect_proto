# requirements

* Docker
* `.env` file with `PREFECT_API_URL` and `PREFECT_API_KEY`

# run

* npm install
* npm run deploy
* npm run invoke

# todo

- [x] external s3 caching
- [x] concurrency=1 for dynamic tags
- [ ] persist results, view history of compute for a given tag
- [ ] explore ui filtering on tags
- [ ] reduce cold boot times (precompile to pyc?)
- [ ] if prefect adds too much overhead, try to read from cache first before interacting with prefect
- [ ] add multiple sub-steps (a, b, c)
- [ ] allocate concurrency on sub-step e.g `id=x & step=a`
- [ ] lambda parameters - skip flag, execute single step, etc.
- [ ] update `get_meaning_task` source code, ensure re-computed on next lazy-eval request
