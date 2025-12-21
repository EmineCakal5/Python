import os
import shutil
from git import Repo

class GitManager:
    def __init__(self, storage_path="/app/storage"):
        self.storage_path = storage_path

    def clone_repo(self, repo_url, test_id): # test_id parametresi eklendi
        try:
            # Örn: libft
            project_name = repo_url.split('/')[-1].replace('.git', '')
            
            # Klasör yapısı: Storage/abc123de/libft
            target_path = os.path.join(self.storage_path, test_id, project_name)

            # Eğer bu test_id ile bir klasör varsa (ki uuid ile zor) temizle
            if os.path.exists(target_path):
                shutil.rmtree(target_path)

            print(f"[{test_id}] Cloning {repo_url}...")
            Repo.clone_from(repo_url, target_path)
            
            return {
                "status": "SUCCESS", 
                "path": target_path, 
                "project": project_name
            }
        except Exception as e:
            return {"status": "FAILURE", "error": str(e)}