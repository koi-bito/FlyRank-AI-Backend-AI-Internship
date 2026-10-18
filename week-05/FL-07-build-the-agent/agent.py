"""
FL-07: RepoArchitect — Autonomous Codebase Inspector Agent
Connects to real local filesystem tools, executes an autonomous reasoning loop,
and produces a structured architectural specification while obeying strict safety guardrails.
"""
import os
import sys
import glob
import re
import json
from typing import Dict, Any, List

class LocalToolRegistry:
    """Local MCP-compliant tool execution registry for the agent."""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = os.path.abspath(workspace_root)

    def _resolve_safe_path(self, rel_path: str) -> str:
        safe_path = os.path.abspath(os.path.join(self.workspace_root, rel_path))
        if not safe_path.startswith(self.workspace_root):
            raise PermissionError(f"Access denied: Path {rel_path} escapes workspace boundary")
        return safe_path

    def list_directory(self, rel_dir: str = ".") -> List[str]:
        target = self._resolve_safe_path(rel_dir)
        if not os.path.isdir(target):
            return []
        items = os.listdir(target)
        # Filter out hidden or cache directories
        return [i for i in items if not i.startswith(".") and i not in ["__pycache__", "node_modules", "cache"]]

    def read_file(self, rel_path: str, max_lines: int = 100) -> str:
        path = self._resolve_safe_path(rel_path)
        if not os.path.isfile(path):
            return f"Error: File {rel_path} does not exist"
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines = [f.readline() for _ in range(max_lines)]
                return "".join(lines)
        except Exception as e:
            return f"Error reading {rel_path}: {e}"

    def grep_search(self, pattern: str, rel_dir: str = ".") -> List[Dict[str, Any]]:
        target_dir = self._resolve_safe_path(rel_dir)
        matches = []
        regex = re.compile(pattern, re.IGNORECASE)
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ["node_modules", "__pycache__", "cache"]]
            for file in files:
                if file.endswith((".py", ".js", ".ts", ".json", ".sql", ".md")):
                    full_p = os.path.join(root, file)
                    rel_p = os.path.relpath(full_p, self.workspace_root)
                    try:
                        with open(full_p, "r", encoding="utf-8", errors="ignore") as f:
                            for idx, line in enumerate(f, 1):
                                if regex.search(line):
                                    matches.append({"file": rel_p, "line": idx, "content": line.strip()})
                                    if len(matches) >= 15:
                                        return matches
                    except Exception:
                        pass
        return matches


class RepoArchitectAgent:
    """Autonomous agent executing an iterative loop over local tool primitives."""
    
    def __init__(self, target_directory: str, max_iterations: int = 8):
        self.tools = LocalToolRegistry(target_directory)
        self.max_iterations = max_iterations
        self.history = []

    def execute_audit(self) -> Dict[str, Any]:
        print(f"[*] Starting RepoArchitect Agent on workspace: {self.tools.workspace_root}")
        findings = {
            "entry_point": None,
            "framework": "Unknown",
            "persistence": "None detected",
            "auth": "None detected",
            "security_risks": [],
            "files_analyzed": []
        }
        
        # Step 1: Discover directory structure
        root_files = self.tools.list_directory(".")
        print(f"[Tool: list_directory] Discovered root files: {root_files}")
        
        # Guardrail check: scan for untracked secrets
        if ".env" in os.listdir(self.tools.workspace_root):
            gitignore = self.tools.read_file(".gitignore")
            if ".env" not in gitignore:
                findings["security_risks"].append("CRITICAL: .env file present but NOT listed in .gitignore!")

        # Step 2: Detect Entry Point
        candidates = ["main.py", "app.py", "server.js", "src/index.js", "scraper.py"]
        for cand in candidates:
            if os.path.exists(os.path.join(self.tools.workspace_root, cand)):
                findings["entry_point"] = cand
                findings["files_analyzed"].append(cand)
                break
                
        # Step 3: Inspect Entry Point
        if findings["entry_point"]:
            code_sample = self.tools.read_file(findings["entry_point"], max_lines=40)
            print(f"[Tool: read_file] Ingested entry point {findings['entry_point']}")
            if "FastAPI" in code_sample:
                findings["framework"] = "FastAPI (Python)"
            elif "express" in code_sample.lower():
                findings["framework"] = "Express.js (Node.js)"

        # Step 4: Search for Database & Persistence
        db_matches = self.tools.grep_search("sqlite|postgres|database_url|create table")
        print(f"[Tool: grep_search] Found {len(db_matches)} persistence indicators")
        if db_matches:
            first_match = db_matches[0]
            findings["persistence"] = f"Detected in {first_match['file']} (line {first_match['line']})"
            findings["files_analyzed"].append(first_match["file"])

        # Step 5: Search for Auth & Protected Routes
        auth_matches = self.tools.grep_search("jwt|bearer|authorization|get_current_user")
        if auth_matches:
            findings["auth"] = f"JWT Bearer detected in {auth_matches[0]['file']}"
            findings["files_analyzed"].append(auth_matches[0]["file"])

        return findings

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    agent = RepoArchitectAgent(target)
    report = agent.execute_audit()
    print("\n=== FINAL REPOARCHITECT AUDIT REPORT ===")
    print(json.dumps(report, indent=2))
