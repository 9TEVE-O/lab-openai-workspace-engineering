from __future__ import annotations
import hashlib, json, pathlib, platform, sqlite3, subprocess
from importlib.metadata import version

R0='6a456830ca33eb5edaa634a9b0febe5d71bea2be'
R0_PARENT='a7b734946f95341f52d866321c183e3532ac0aad'
ROADMAP_SHA='2aa4ecbee879f3431ae17795ff7eb9e90c4ae74c67b338cc8ec1566137799ffe'
ARMS={'P-A':'A_END_REVIEW','P-B':'B_SAME_MODEL_REVIEW','P-C':'C_DETERMINISTIC_VERIFICATION','P-D':'D_DECISION_BOUNDARY'}
CONTROL=pathlib.Path('/v0-control')
WORKSPACE=pathlib.Path('/workspace')
EVIDENCE=pathlib.Path('/v0-evidence')

def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()

def run(*args, cwd=None):
    return subprocess.run(args,cwd=cwd,text=True,capture_output=True,check=False)

def git_run(repo, *args):
    # The trajectory repositories are host-created read-only mounts. Explicitly
    # declare only the inspected repository path safe for this command; do not
    # use a wildcard and do not modify the mounted repository or global config.
    return run('git','-c',f'safe.directory={repo}',*args,cwd=repo)

def rendered(result):
    stdout=result.stdout.strip()
    stderr=result.stderr.strip()
    if result.returncode == 0:
        return stdout
    return f'EXIT_{result.returncode}: {stderr or stdout or "NO_OUTPUT"}'

def add(checks,name,ok,expected=None,actual=None):
    checks.append({'check':name,'status':'PASS' if ok else 'FAIL','expected':expected,'actual':actual})
    return ok

def main():
    EVIDENCE.mkdir(parents=True,exist_ok=True)
    manifest_path=CONTROL/'P1_ENVIRONMENT_MANIFEST_RESTORED_v0.1.json'
    profile_path=CONTROL/'EXECUTOR_PARITY_PROFILE_v0.1.json'
    binding_path=CONTROL/'V0_BINDING_v0.1.json'
    manifest=json.loads(manifest_path.read_text())
    profile=json.loads(profile_path.read_text())
    binding=json.loads(binding_path.read_text())
    mh=sha(manifest_path); ph=sha(profile_path)
    env_checks=[]
    add(env_checks,'python',platform.python_version()==manifest['python'],manifest['python'],platform.python_version())
    add(env_checks,'sqlite_runtime',sqlite3.sqlite_version==manifest['sqlite_runtime'],manifest['sqlite_runtime'],sqlite3.sqlite_version)
    add(env_checks,'setuptools',version('setuptools')==manifest['setuptools'],manifest['setuptools'],version('setuptools'))
    add(env_checks,'pip',version('pip')==manifest['pip'],manifest['pip'],version('pip'))
    git_version=run('git','--version')
    gv=git_version.stdout.strip().split()[-1] if git_version.returncode==0 else rendered(git_version)
    add(env_checks,'git',git_version.returncode==0 and gv==manifest['git'],manifest['git'],gv)
    gcc_result=run('gcc','--version')
    gcc=gcc_result.stdout.splitlines()[0] if gcc_result.returncode==0 else rendered(gcc_result)
    add(env_checks,'gcc',gcc_result.returncode==0 and manifest['gcc'] in gcc,manifest['gcc'],gcc)
    for name, expected in manifest['control_file_sha256'].items():
        p=(pathlib.Path('/p1-control')/'requirements.exact.txt') if name=='requirements.exact.txt' else (pathlib.Path('/control')/name)
        add(env_checks,f'control_hash:{name}',p.exists() and sha(p)==expected,expected,sha(p) if p.exists() else 'MISSING')
    add(env_checks,'p1_manifest_binding',profile['p1_environment_manifest_sha256']==mh,mh,profile['p1_environment_manifest_sha256'])
    add(env_checks,'roadmap_profile',profile['roadmap_sha256']==ROADMAP_SHA,ROADMAP_SHA,profile['roadmap_sha256'])
    add(env_checks,'roadmap_binding',binding['roadmap_sha256']==ROADMAP_SHA,ROADMAP_SHA,binding['roadmap_sha256'])
    add(env_checks,'profile_binding',binding['executor_parity_profile_sha256']==ph,ph,binding['executor_parity_profile_sha256'])
    add(env_checks,'manifest_binding',binding['p1_environment_manifest_sha256']==mh,mh,binding['p1_environment_manifest_sha256'])
    add(env_checks,'system_instruction_hash',sha(CONTROL/'EXECUTOR_SYSTEM_v0.1.txt')==profile['instruction_sha256']['system'],profile['instruction_sha256']['system'],sha(CONTROL/'EXECUTOR_SYSTEM_v0.1.txt'))
    add(env_checks,'developer_instruction_hash',sha(CONTROL/'EXECUTOR_DEVELOPER_v0.1.txt')==profile['instruction_sha256']['developer'],profile['instruction_sha256']['developer'],sha(CONTROL/'EXECUTOR_DEVELOPER_v0.1.txt'))
    records=[]
    for arm, condition in ARMS.items():
        checks=list(env_checks)
        repo=WORKSPACE/arm/'sqlite-utils'
        head_r=git_run(repo,'rev-parse','HEAD')
        parent_r=git_run(repo,'rev-parse','HEAD^')
        status_r=git_run(repo,'status','--porcelain=v1')
        branch_r=git_run(repo,'symbolic-ref','-q','--short','HEAD')
        head=head_r.stdout.strip()
        parent=parent_r.stdout.strip()
        status=status_r.stdout
        add(checks,'r0_head',head_r.returncode==0 and head==R0,R0,rendered(head_r))
        add(checks,'r0_parent',parent_r.returncode==0 and parent==R0_PARENT,R0_PARENT,rendered(parent_r))
        add(checks,'worktree_clean',status_r.returncode==0 and status=='','',rendered(status_r))
        # git symbolic-ref -q returns exactly 1 for a detached HEAD. Any other
        # non-zero result is an inspection failure and must not masquerade as detached.
        add(checks,'detached_head',branch_r.returncode==1,'DETACHED','DETACHED' if branch_r.returncode==1 else rendered(branch_r))
        add(checks,'condition_binding',profile['conditions'].get(arm)==condition,condition,profile['conditions'].get(arm))
        ok=all(c['status']=='PASS' for c in checks)
        rec={'schema_version':1,'verification_layer':'V0','scope':'PREFLIGHT_ONLY_NO_FEATURE_EXECUTION','arm':arm,'condition':condition,'status':'PASS' if ok else 'INVALID','r0_commit':R0,'r0_parent':R0_PARENT,'worktree':str(repo),'worktree_status_porcelain':status if status_r.returncode==0 else rendered(status_r),'roadmap_sha256':ROADMAP_SHA,'p1_environment_manifest_sha256':mh,'executor_parity_profile_sha256':ph,'checks':checks}
        (EVIDENCE/f'V0_{arm}.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
        records.append(rec)
    summary={'schema_version':1,'verification_layer':'V0','scope':'PREFLIGHT_ONLY_NO_FEATURE_EXECUTION','overall_status':'PASS' if all(r['status']=='PASS' for r in records) else 'INVALID','feature_trajectory_execution':'NOT_STARTED','arms':{r['arm']:r['status'] for r in records},'p1_environment_manifest_sha256':mh,'executor_parity_profile_sha256':ph,'roadmap_sha256':ROADMAP_SHA}
    (EVIDENCE/'V0_SUMMARY.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
    print(json.dumps(summary,sort_keys=True,indent=2))
    return 0 if summary['overall_status']=='PASS' else 1

if __name__=='__main__':
    raise SystemExit(main())
