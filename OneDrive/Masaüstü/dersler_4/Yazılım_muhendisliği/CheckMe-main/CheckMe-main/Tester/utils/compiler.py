import subprocess
import os
import re

class Compiler:
    def __init__(self):
        self.flags = ["-Wall", "-Wextra", "-Werror"]

    def run_command(self, cmd, path):
        return subprocess.run(cmd, cwd=path, capture_output=True, text=True)

    def check_all(self, path, expected_name="push_swap"):
        results = []
        
        if not os.path.exists(os.path.join(path, "Makefile")):
            return [{"id": 2, "status": "KO", "msg": "Makefile missing"}]
        results.append({"id": 2, "status": "OK"})

        with open(os.path.join(path, "Makefile"), 'r') as f:
            content = f.read()

            for rule in ["all:", "clean:", "fclean:", "re:"]:
                if rule not in content.replace(" ", ""):
                    results.append({"id": 3, "status": "KO", "msg": f"Missing {rule}"})
                    return results
            results.append({"id": 3, "status": "OK"})

            if all(flag in content for flag in self.flags):
                results.append({"id": 4, "status": "OK"})
            else:
                results.append({"id": 4, "status": "KO", "msg": "Missing flags"})

        self.run_command(["make", "fclean"], path)
        compile_res = self.run_command(["make"], path)
        
        if compile_res.returncode == 0 and os.path.exists(os.path.join(path, expected_name)):
            results.append({"id": 5, "status": "OK"})
        else:
            # Capture output
            error_details = f"Return Code: {compile_res.returncode}\nStdout: {compile_res.stdout[:500]}\nStderr: {compile_res.stderr[:500]}"
            results.append({"id": 5, "status": "KO", "msg": "Build failed", "errors": error_details})
            return results

        relink_res = self.run_command(["make"], path)
        if "make: Nothing to be done" in relink_res.stdout or "is up to date" in relink_res.stdout:
            results.append({"id": 6, "status": "OK"})
        else:
            results.append({"id": 6, "status": "KO", "msg": "Relink detected"})

        return results