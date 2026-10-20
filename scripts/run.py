"""Map a unified diff to focused review areas and verification needs."""
from runtime import *

import re
import ast

def git_path(value):
    if value.startswith('"'):
        try:
            decoded = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ValueError("invalid quoted Git path") from exc
        if not isinstance(decoded, str): raise ValueError("invalid Git path")
        try: value = decoded.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError): value = decoded
    return value

def process(data):
    diff=data["diff"]
    if not isinstance(diff,str): raise ValueError("diff must be text")
    files=[]
    current=None
    old_path=None
    in_hunk=False
    old_left=new_left=0
    rules={"authentication":r"auth|permission|session|credential","persistence":r"migrat|schema|database|storage","dependencies":r"lock|requirements|package\.json|pyproject","tests":r"(^|/)(test|tests|spec)|\.test\.|\.spec\."}
    for line in diff.split("\n"):
        if line.startswith("diff --git "):
            if old_left or new_left: raise ValueError("truncated diff hunk")
            match=re.fullmatch(r'diff --git ("(?:\\.|[^"])*"|a/.*?) ("(?:\\.|[^"])*"|b/.*)',line)
            if match is None: raise ValueError("unsupported diff header")
            path=git_path(match.group(2))
            if line.startswith("diff --git a/"):
                header=line[len("diff --git "):]
                for split in re.finditer(" b/",header):
                    left,right=header[:split.start()],header[split.start()+1:]
                    if left[2:]==right[2:]:
                        path=right
                        break
            if path.startswith("b/"): path=path[2:]
            old_path=None
            current={"path":path,"additions":0,"deletions":0,"review_areas":[k for k,p in rules.items() if re.search(p,path,re.I)]}
            files.append(current)
            in_hunk=False
        elif line.startswith("@@ "):
            if current is None: raise ValueError("hunk without git file header")
            if old_left or new_left: raise ValueError("truncated diff hunk")
            match=re.match(r"@@ -\d+(?:,(\d+))? \+\d+(?:,(\d+))? @@",line)
            if match is None: raise ValueError("invalid diff hunk header")
            old_left=int(match.group(1) or "1")
            new_left=int(match.group(2) or "1")
            in_hunk=True
        elif in_hunk and current is not None:
            if line.startswith("\\ No newline"): continue
            if line.startswith("+"):
                current["additions"]+=1
                new_left-=1
            elif line.startswith("-"):
                current["deletions"]+=1
                old_left-=1
            elif line.startswith(" "):
                old_left-=1
                new_left-=1
            else: raise ValueError("invalid diff hunk line")
            if old_left<0 or new_left<0: raise ValueError("diff hunk exceeds its declared size")
            in_hunk=bool(old_left or new_left)
        elif current is not None and line.startswith("--- "):
            old_path=git_path(line[4:].split("\t",1)[0])
        elif current is not None and line.startswith("+++ "):
            path=git_path(line[4:].split("\t",1)[0])
            if path=="/dev/null": path=old_path or current["path"]
            current["path"]=path[2:] if path.startswith(("a/","b/")) else path
            current["review_areas"]=[k for k,p in rules.items() if re.search(p,current["path"],re.I)]
        elif current is not None and line.startswith("rename to "):
            current["path"]=git_path(line[len("rename to "):])
            current["review_areas"]=[k for k,p in rules.items() if re.search(p,current["path"],re.I)]
        elif current is not None and line[:1] in ("+","-"," "):
            raise ValueError("diff hunk exceeds its declared size")
    if old_left or new_left: raise ValueError("truncated diff hunk")
    if diff.strip() and not files: raise ValueError("no git diff headers found")
    return {"files":files,"additions":sum(x["additions"] for x in files),"deletions":sum(x["deletions"] for x in files)}

if __name__ == "__main__":
    sys.exit(main(process, "Map a unified diff to focused review areas and verification needs."))
