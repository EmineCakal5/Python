# CheckMe Tester Service

This service is the core testing engine for the CheckMe platform. It handles repository cloning, compilation checks, and logic testing for 42 School projects (starting with `push_swap`).

## Features

- **Automated Testing**: Clones student repositories and runs a battery of tests.
- **Push_Swap Logic**: Validates sorting correctness, move counts, and memory leaks (Valgrind).
- **REST API**: Exposes endpoints for triggering tests and retrieving results.
- **Dockerized**: runs in an isolated container environment.

## API Endpoints

### `POST /test`
Triggers a full test cycle (Clone -> Compile -> Logic Tests).
**Request:**
```json
{ "repo_url": "https://github.com/user/push_swap.git" }
```

### `POST /test/logic`
Runs only logic tests on an existing repo.
**Request:**
```json
{ "repo_path": "/app/storage/test_id", "test_type": "full" }
```

## detailed Testing Steps

1.  **Clone**: Clones the repository using Git.
2.  **Makefile Check**: Verifies existence of Makefile and required rules (all, clean, fclean, re).
3.  **Compilation**: Runs `make` and checks for executable creation.
4.  **Relink Check**: Runs `make` again to ensure no unnecessary recompilation.
5.  **Logic Tests**:
    - **Random Numbers**: Tests with 3, 5, 100, 500 numbers.
    - **Edge Cases**: Empty, existing duplicates, max/min integers.
    - **Memory Leaks**: Checks with Valgrind.

## Directory Structure

- `main.py`: FastAPI entry point.
- `utils/`: Generic helpers (Git, Compiler, Number Generator).

## Health Check & Logging

### Health Check
Verify the service is running:
```bash
curl http://localhost:8000/health
# Output: {"status":"ok","service":"push_swap-tester"}
```

### Viewing Logs
The service logs all requests to `stdout` (docker logs). 

**Per-Test Logs**:
Each test generates a dedicated log file inside its storage folder:
`Storage/{TEST_ID}/test.log` (on your host machine).

This file contains detailed execution logs, compilation errors, and validation reasons for that specific test run.

```bash
docker logs -f checkme-tester
# Or view a specific test log:
cat Storage/a1b2c3d4/test.log
```

### Manual Testing
You can manually trigger a test via curl:
```bash
curl -X POST http://localhost:8000/test \
     -H "Content-Type: application/json" \
     -d '{"repo_url":"https://github.com/myuser/push_swap.git"}'
```
