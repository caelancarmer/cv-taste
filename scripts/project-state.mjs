#!/usr/bin/env node
// Project-state v2: local checkpoint helper. No network, merge, deploy or automatic task replay.
import { existsSync, readFileSync, writeFileSync, renameSync, openSync, closeSync, unlinkSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { randomUUID } from 'node:crypto';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const loc=p=>resolve(root,p);
const paths=[
 'AGENTS.md','project-state/README.md','project-state/current-state.md',
 'project-state/decisions.md','project-state/open-tasks.md','project-state/handoff.md',
 'project-state/evidence/README.md','project-state/recovery/recovery-policy.md',
 'project-state/recovery/last-checkpoint.json','project-state/recovery/active-execution.json',
 'project-state/sessions/session-index.json'
];
const idRe=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const shaRe=/^[a-f0-9]{40}$/;
const repoName=()=>{const s=readFileSync(loc('project-state/current-state.md'),'utf8');const m=s.match(/^- repository: \x60?(caelancarmer\/[a-z0-9-]+)\x60?$/m);if(!m)throw Error('repository identity missing in current-state.md');return m[1];};
const read=p=>JSON.parse(readFileSync(loc(p),'utf8'));
const atomic=(p,data)=>{const target=loc(p),tmp=target+'.tmp-'+process.pid+'-'+randomUUID();writeFileSync(tmp,JSON.stringify(data,null,2)+'\n',{flag:'wx',mode:0o600});renameSync(tmp,target);};
const head=()=>execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
const lock=fn=>{const f=loc('project-state/recovery/.writer.lock');let fd;try{fd=openSync(f,'wx');writeFileSync(fd,JSON.stringify({pid:process.pid,created_at:new Date().toISOString()})+'\n');return fn();}finally{if(fd!==undefined){closeSync(fd);unlinkSync(f);}}};
function inspect(){
 const problems=[];
 for(const p of paths){if(!existsSync(loc(p))){problems.push('missing '+p);continue;}const s=readFileSync(loc(p),'utf8');if(s.trim().length<4)problems.push('empty '+p);if(/^(<{7}|={7}|>{7})/m.test(s))problems.push('merge marker '+p);}
 if(problems.length)return {ok:false,problems};
 try{
 const repo=repoName(),cp=read('project-state/recovery/last-checkpoint.json'),a=read('project-state/recovery/active-execution.json'),sessions=read('project-state/sessions/session-index.json');
 if(cp.schema_version!==2||a.schema_version!==2||sessions.schema_version!==2)problems.push('schema version != 2');
 if(cp.repository!==repo||a.repository!==repo||sessions.repository!==repo)problems.push('repository identity mismatch');
 if(!Number.isInteger(cp.sequence)||cp.sequence<0||typeof cp.checkpoint_id!=='string')problems.push('invalid checkpoint identity');
 if(!shaRe.test(cp.source_sha))problems.push('invalid checkpoint source SHA');
 if(!Array.isArray(sessions.sessions)||typeof sessions.last_checkpoint_id!=='string')problems.push('invalid session index');
 if(sessions.last_checkpoint_id!==cp.checkpoint_id)problems.push('session index and checkpoint diverged; reconcile before using');
 if(a.active!==null && (!a.active||typeof a.active.attempt_id!=='string'||!shaRe.test(a.active.source_sha)))problems.push('invalid active execution');
 const agents=readFileSync(loc('AGENTS.md'),'utf8');
 if(!agents.includes('Project-state v2 preflight'))problems.push('AGENTS.md missing v2 rule');
 return {ok:problems.length===0,problems,repository:repo,checkpoint_id:cp.checkpoint_id,sequence:cp.sequence,active_attempt:a.active?.attempt_id??null,agent_compliance_proven:false,external_proof_verified:false};
 }catch(e){return {ok:false,problems:[...problems,String(e.message)]};}
}
function recovery(){
 const x=inspect();
 if(!x.ok)return {...x,decision:'STOP_AND_RECONCILE',automatic_retry:false};
 const cp=read('project-state/recovery/last-checkpoint.json'),a=read('project-state/recovery/active-execution.json');
 let checkout=null;
 try{checkout=head();}catch{}
 return {...x,checkout_sha:checkout,checkpoint_source_sha:cp.source_sha,last_result:cp.result??'baseline-only',
 decision:a.active?'INSPECT_INTERRUPTED_ATTEMPT':'VERIFY_LIVE_GIT_PR_CI_BEFORE_WORK',
 reason:a.active?'An active attempt may have produced external effects; inspect receipts before any retry.':'Checkpoint is a starting point, not a live oracle.',
 automatic_retry:false,automatic_merge:false};
}
function begin(sessionId,taskId,expectedSha){
 const s=inspect();if(!s.ok)throw Error('State invalid: '+s.problems.join('; '));
 if(!idRe.test(sessionId)||!idRe.test(taskId)||!shaRe.test(expectedSha))throw Error('Use kebab-case session/task IDs and a full 40-char source SHA');
 if(head()!==expectedSha)throw Error('Checkout HEAD differs from expected SHA; refresh evidence before starting');
 const a=read('project-state/recovery/active-execution.json');if(a.active)throw Error('Existing attempt must be reconciled; no implicit replay');
 const cp=read('project-state/recovery/last-checkpoint.json'),sessions=read('project-state/sessions/session-index.json');
 const attempt={attempt_id:randomUUID(),session_id:sessionId,task_id:taskId,source_sha:expectedSha,started_at:new Date().toISOString(),base_checkpoint_id:cp.checkpoint_id,status:'in-progress',external_effects:'unknown'};
 a.active=attempt;
 // Active file is written first, so a crash fails closed and is visible to recovery.
 atomic('project-state/recovery/active-execution.json',a);
 sessions.sessions.push({session_id:sessionId,attempt_id:attempt.attempt_id,task_id:taskId,started_at:attempt.started_at,result:'in-progress'});
 atomic('project-state/sessions/session-index.json',sessions);
 return {attempt_id:attempt.attempt_id,status:'in-progress',next:'execute only independently authorized actions; checkpoint with evidence'};
}
function close(result,evidenceRef){
 const choices=new Set(['reported-pass','failed','blocked','unknown']);
 if(!choices.has(result)||typeof evidenceRef!=='string'||evidenceRef.length<5||evidenceRef.length>500||/[\x00-\x1f]/.test(evidenceRef))throw Error('close requires result reported-pass|failed|blocked|unknown and a non-secret evidence reference');
 const a=read('project-state/recovery/active-execution.json'),cp=read('project-state/recovery/last-checkpoint.json'),sessions=read('project-state/sessions/session-index.json');
 if(!a.active)throw Error('No active execution; no fabricated completion');
 const attempt=a.active;
 if(sessions.last_checkpoint_id!==cp.checkpoint_id)throw Error('Checkpoint/session index mismatch; reconcile manually');
 const when=new Date().toISOString();
 const next={schema_version:2,repository:repoName(),sequence:cp.sequence+1,checkpoint_id:randomUUID(),previous_checkpoint_id:cp.checkpoint_id,source_sha:head(),observed_at:when,status:'agent-reported',result,attempt_id:attempt.attempt_id,session_id:attempt.session_id,task_id:attempt.task_id,evidence_ref:evidenceRef,independent_evidence_verified:false,external_effects:'requires-independent-reconciliation'};
 // Checkpoint is committed first. If the process dies, 'recover' flags the disagreement.
 atomic('project-state/recovery/last-checkpoint.json',next);
 a.active=null;atomic('project-state/recovery/active-execution.json',a);
 const ix=sessions.sessions.findLastIndex(x=>x.attempt_id===attempt.attempt_id);
 if(ix<0)throw Error('Missing session receipt after checkpoint write; reconcile manually');
 sessions.sessions[ix]={...sessions.sessions[ix],result,closed_at:when,checkpoint_id:next.checkpoint_id,evidence_ref:evidenceRef};
 sessions.last_checkpoint_id=next.checkpoint_id;
 atomic('project-state/sessions/session-index.json',sessions);
 return {checkpoint_id:next.checkpoint_id,result,independent_evidence_verified:false,next:'update current-state.md, open-tasks.md and handoff.md; commit/push review branch with source evidence'};
}
const [command='verify',a,b,c]=process.argv.slice(2);
try{
 let result;
 if(command==='verify')result=inspect();
 else if(command==='recover')result=recovery();
 else if(command==='begin')result=lock(()=>begin(a,b,c));
 else if(command==='close')result=lock(()=>close(a,b));
 else throw Error('Commands: verify | recover | begin <session-id> <task-id> <expected-head-sha> | close <reported-pass|failed|blocked|unknown> <evidence-ref>');
 console.log(JSON.stringify(result,null,2));
 if(result.ok===false)process.exitCode=1;
}catch(e){console.error('PROJECT-STATE-HELD: '+e.message);process.exitCode=1;}
