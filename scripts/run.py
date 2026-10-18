"""Map a unified diff to focused review areas and verification needs."""
from runtime import *

import re
import shlex
def process(data):
    diff=data["diff"]
    if not isinstance(diff,str): raise ValueError("diff must be text")
    files=[]
    current=None
    in_hunk=False
    rules={"authentication":r"auth|permission|session|credential","persistence":r"migrat|schema|database|storage","dependencies":r"lock|requirements|package\.json|pyproject","tests":r"(^|/)(test|tests|spec)|\.test\.|\.spec\."}
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            parts=shlex.split(line)
            if len(parts)!=4: raise ValueError("unsupported diff header")
            path=parts[3][2:] if parts[3].startswith("b/") else parts[3]
            current={"path":path,"additions":0,"deletions":0,"review_areas":[k for k,p in rules.items() if re.search(p,path,re.I)]}
            files.append(current)
            in_hunk=False
        elif line.startswith("@@ "):
            if current is None: raise ValueError("hunk without git file header")
            in_hunk=True
        elif in_hunk and current is not None:
            if line.startswith("+"): current["additions"]+=1
            elif line.startswith("-"): current["deletions"]+=1
    if diff.strip() and not files: raise ValueError("no git diff headers found")
    return {"files":files,"additions":sum(x["additions"] for x in files),"deletions":sum(x["deletions"] for x in files)}

if __name__ == "__main__":
    sys.exit(main(process, "Map a unified diff to focused review areas and verification needs."))
