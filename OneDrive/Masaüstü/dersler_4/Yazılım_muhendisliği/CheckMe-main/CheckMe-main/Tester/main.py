import uuid
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from utils.git_manager import GitManager
from utils.compiler import Compiler
from strategies.push_swap.logic import PushSwapLogicTester
from utils.number_generator import NumberGenerator
from strategies.push_swap.integration import PushSwapIntegrationTester

import logging
import time
from starlette.requests import Request
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("tester")

app = FastAPI()
git_manager = GitManager()
compiler = Compiler()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TestRequest(BaseModel):
    repo_url: str

class LogicTestRequest(BaseModel):
    repo_path: str
    test_type: str = "full"  # 'quick', 'full', 'performance'
    seed: Optional[int] = None

class CustomTestRequest(BaseModel):
    repo_path: str
    numbers: str
    test_name: str = "custom"

@app.post("/test")
async def start_test(request: TestRequest):
    test_id = str(uuid.uuid4())[:8]
    
    # SETUP PER-TEST LOGGING
    # Create test directory explicitly to hose the log file
    test_dir = f"/app/storage/{test_id}"
    os.makedirs(test_dir, exist_ok=True)
    
    log_file = os.path.join(test_dir, "test.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(file_handler)
    
    try:
        logger.info(f"Starting test {test_id} for repo: {request.repo_url}")
        
        # Adım 1: Clone
        clone_res = git_manager.clone_repo(request.repo_url, test_id)
        if clone_res["status"] == "FAILURE":
            logger.error(f"Clone failed for {test_id}")
            return {"test_id": test_id, "result": {"status": "FAILURE"}, "steps": [{"id": 1, "status": "KO", "msg": "Clone Failed"}]}
        
        # Adım 2-6: Makefile ve Derleme Testleri
        repo_path = clone_res["path"]
        
        # Use IntegrationTester to run everything (compilation + logic)
        tester = PushSwapIntegrationTester(repo_path)
        # Run in "quick" mode by default for the main test endpoint to keep it responsive
        results = tester.run_complete_test(test_type="quick")
        
        # Extract steps from results for frontend compatibility
        test_steps = [{"id": 1, "status": "OK", "msg": "Clone Successful"}] # Clone successful
        
        # Add compilation steps
        if results.get("compilation", {}).get("details"):
            test_steps.extend(results["compilation"]["details"])
        
        # Add logic test summary as a step
        logic_summary = results.get("summary", {})
        logic_status = logic_summary.get("overall_status", "UNKNOWN")
        
        # Detailed Steps for each random test case
        logic_tests_data = results.get("logic_tests") or {}
        logic_results = logic_tests_data.get("results", [])
        
        # Sort results to have small tests first
        # This assumes test_name is sortable or fixed list
        
        step_id_counter = 7
        for res in logic_results:
            test_name = res.get("test_name", "Unknown")
            status = res.get("status", "KO")
            input_count = res.get("number_count", 0)
            
            # Format message
            msg = f"Logic Test: {test_name}"
            if status != "OK":
                if res.get("error"):
                    msg += " (Output Error)"
                elif res.get("validation", {}).get("status") != "OK":
                    msg += f" (Checker: {res.get('validation', {}).get('status')})"
                else:
                    msg += f" (Moves: {res.get('moves')})"
            else:
                 msg += f" (Passed, {res.get('moves')} moves)"
                 
            test_steps.append({
                "id": step_id_counter,
                "status": status,
                "msg": msg
            })
            step_id_counter += 1
    
        if results.get("compilation", {}).get("status") != "OK":
             comp_res = results.get("compilation", {})
             logger.error(f"Test {test_id} compilation failed.")
             # Extract error details from the specific failed step if available & log it
             details = comp_res.get("details", [])
             for step in details:
                 if step.get("status") != "OK" and step.get("errors"):
                     logger.error(f"Step {step['id']} Details:\n{step['errors']}")
        
        # LOG ALL RESULTS (SUCCESS OR FAILURE)
        for res in logic_results:
             # Determine "Actual" reason
             actual = "Unknown"
             if res.get("status") == "OK":
                 actual = f"OK (Moves: {res.get('moves')})"
             elif res.get("error"):
                 actual = f"Error in output (stderr: {res.get('stderr', '')})"
             elif res.get("validation", {}).get("status") != "OK":
                 actual = f"Checker: {res.get('validation', {}).get('message', 'KO')}"
             elif res.get("leak") is False:
                 actual = "Memory Leak Detected"
             elif res.get("status") == "KO":
                 actual = f"KO (Moves: {res.get('moves')})"
             
             log_level = logging.INFO if res.get("status") == "OK" else logging.WARNING
             
             logger.log(
                 log_level,
                 f"\n[TEST DETAIL] Test {test_id}\n"
                 f"  Case:     {res.get('test_name')}\n"
                 f"  Input:    {res.get('input')}\n"
                 f"  Expected: OK (Sorted & Valid Moves)\n"
                 f"  Actual:   {actual}\n"
                 f"  Status:   {res['status']}\n"
             )
        
        final_status = "SUCCESS" if logic_status == "SUCCESS" else "FAILURE"
        
        logger.info(f"Test {test_id} completed with status: {final_status}")
        
        return {
            "test_id": test_id,
            "result": {
                "project": clone_res["project"], 
                "status": final_status,
                "logic_summary": logic_summary,
                "grade": results.get("grade")
            },
            "steps": test_steps
        }
    finally:
        # Cleanup logger handler
        logger.removeHandler(file_handler)
        file_handler.close()

@app.post("/test/logic")
async def run_logic_test(request: LogicTestRequest):
    """
    Run comprehensive logic tests on push_swap executable.
    Tests include: execution, validation with checker, memory leaks, and performance.
    """
    try:
        tester = PushSwapLogicTester(request.repo_path)
        number_gen = NumberGenerator(seed=request.seed)
        
        test_cases = {}
        
        if request.test_type == "quick":
            # Quick test with small cases
            test_cases = {
                "small_3": number_gen.generate_random_numbers(3),
                "small_5": number_gen.generate_random_numbers(5),
                "edge_limits": number_gen.generate_edge_case_numbers("limits"),
            }
        
        elif request.test_type == "full":
            # Full test suite
            test_cases = {
                "small_3": number_gen.generate_random_numbers(3),
                "small_5": number_gen.generate_random_numbers(5),
                "medium_100": number_gen.generate_random_numbers(100),
                "large_500": number_gen.generate_random_numbers(500),
                "edge_negative": number_gen.generate_edge_case_numbers("negative"),
                "edge_positive": number_gen.generate_edge_case_numbers("positive"),
                "edge_limits": number_gen.generate_edge_case_numbers("limits"),
                "edge_mixed": number_gen.generate_edge_case_numbers("mixed"),
            }
        
        elif request.test_type == "performance":
            # Performance-focused tests
            test_cases = {
                "perf_100": number_gen.generate_random_numbers(100),
                "perf_500": number_gen.generate_random_numbers(500),
            }
        
        results = tester.run_test_suite(test_cases)
        
        # Calculate summary
        total_tests = len(results)
        passed_tests = sum(1 for r in results if r["status"] == "OK")
        no_leaks = sum(1 for r in results if r["leak"] is True)
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "memory_safe": no_leaks,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
        }
        
        return {
            "test_type": request.test_type,
            "summary": summary,
            "results": results
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "test_type": request.test_type,
            "summary": None,
            "results": []
        }

@app.post("/test/custom")
async def run_custom_test(request: CustomTestRequest):
    """
    Run a custom test with specific numbers.
    """
    try:
        tester = PushSwapLogicTester(request.repo_path)
        result = tester.run_single_test(request.numbers, request.test_name)
        
        return {
            "test_name": request.test_name,
            "result": result,
            "success": result["status"] == "OK"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "test_name": request.test_name,
            "result": None,
            "success": False
        }

@app.get("/test/generate/{count}")
async def generate_test_numbers(count: int, edge_case: Optional[str] = None):
    """
    Generate test numbers.
    
    Args:
        count: Number of integers to generate (3, 5, 100, 500)
        edge_case: Optional edge case type (negative, positive, limits, mixed, duplicates)
    """
    try:
        gen = NumberGenerator()
        
        if edge_case:
            numbers = gen.generate_edge_case_numbers(edge_case)
            test_type = f"edge_{edge_case}"
        else:
            numbers = gen.generate_random_numbers(count)
            test_type = f"random_{count}"
        
        return {
            "test_type": test_type,
            "numbers": numbers,
            "count": len(numbers.split()),
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "numbers": "",
            "count": 0
        }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "push_swap-tester"}

@app.post("/test/integration")
async def run_integration_test(request: LogicTestRequest):
    """
    Run complete integration test: compilation + logic tests + grading.
    """
    try:
        tester = PushSwapIntegrationTester(request.repo_path)
        results = tester.run_complete_test(
            test_type=request.test_type,
            seed=request.seed
        )
        
        # Calculate grade
        grade = tester.get_grade(results)
        results["grade"] = grade
        
        return results
    
    except Exception as e:
        return {
            "error": str(e),
            "compilation": None,
            "logic_tests": None,
            "grade": {"grade": "F", "reason": f"Error: {str(e)}"},
            "summary": {"overall_status": "ERROR"}
        }