// Camel cycle receipt admission: static claim validation, NOT external attestation.
const SHA=/^[a-f0-9]{40}$/;
const ID=/^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const REPO=/^[a-z0-9-]+\/[a-z0-9-]+$/;
const STATUS=new Set(['COMMITTED','VERIFIED_PASS','FAILED','BLOCKED','NOT_RUN']);
const QA=new Set(['PASS','FAIL','NOT_RUN']);
const CAT=new Set(['engineering','research','blocker']);
const obj=x=>x!==null&&typeof x==='object'&&!Array.isArray(x)&&Object.getPrototypeOf(x)===Object.prototype;
const only=(x,keys)=>Object.keys(x).every(k=>keys.includes(k));
const safe=x=>typeof x==='string'&&x.length>0&&x.length<=500&&x.trim()===x&&!/[\x00-\x1f\x7f]/.test(x);
export function auditCycle(cycle){
 const errors=[],out={schema_version:1,valid:false,errors,per_repository:[],total_native_claims:0,
  authoritative_evidence_verified:false,host_hook_verified:false};
 const err=(where,why)=>errors.push(where+': '+why);
 if(!obj(cycle)||!only(cycle,['schema_version','cycle_id','projects'])){err('cycle','invalid root/unknown field');return out;}
 if(cycle.schema_version!==1||!ID.test(cycle.cycle_id||''))err('cycle','invalid schema or cycle id');
 if(!Array.isArray(cycle.projects)||cycle.projects.length<1||cycle.projects.length>25){err('projects','require 1..25');return out;}
 const seen=[];
 for(const [i,p] of cycle.projects.entries()){
  const loc='projects['+i+']';
  if(!obj(p)||!only(p,['repo','requested_tasks','source_sha','tasks','checkpoint'])){err(loc,'invalid project fields');continue;}
  if(!REPO.test(p.repo||''))err(loc,'invalid repo');seen.push(p.repo);
  if(!SHA.test(p.source_sha||''))err(loc,'exact 40-char SHA required');
  if(!Number.isInteger(p.requested_tasks)||p.requested_tasks<1||p.requested_tasks>20)err(loc,'invalid per-repo budget');
  if(!Array.isArray(p.tasks)||p.tasks.length>p.requested_tasks){err(loc,'tasks exceed per-repository budget');continue;}
  if(!obj(p.checkpoint)||!only(p.checkpoint,['status','ref'])||
   !['PERSISTED','NOT_SAVED'].includes(p.checkpoint.status)||
   (p.checkpoint.status==='PERSISTED'&&!safe(p.checkpoint.ref)))err(loc,'invalid checkpoint status/ref');
  let native=0,attempted=0;const ids=[];
  for(const [j,t] of p.tasks.entries()){
   const where=loc+'.tasks['+j+']';
   if(!obj(t)||!only(t,['id','category','status','changed_paths','commit_sha','verification_sha','qa','evidence','next_action','blocker'])){err(where,'invalid task fields');continue;}
   if(!ID.test(t.id||''))err(where,'invalid task ID');ids.push(t.id);
   if(!CAT.has(t.category)||!STATUS.has(t.status)||!QA.has(t.qa))err(where,'unknown task category/status/QA');
   if(!Array.isArray(t.changed_paths)||t.changed_paths.length>100||t.changed_paths.some(v=>!safe(v)||v.startsWith('/')||v.includes('..')))err(where,'invalid changed path');
   if(!Array.isArray(t.evidence)||t.evidence.length>30||t.evidence.some(v=>!safe(v)))err(where,'invalid evidence ref');
   if(t.status!=='NOT_RUN')attempted++;
   if(['COMMITTED','VERIFIED_PASS'].includes(t.status)){
    if(t.category!=='engineering'||!t.changed_paths?.length||!SHA.test(t.commit_sha||''))err(where,'native DONE requires source deliverable plus commit SHA');
    else native++;
   }
   if(t.status==='VERIFIED_PASS'&&(t.qa!=='PASS'||!SHA.test(t.verification_sha||'')||t.verification_sha!==t.commit_sha||!t.evidence?.length))err(where,'PASS requires evidence on same SHA');
   if(t.status==='COMMITTED'&&t.qa==='PASS'&&t.verification_sha!==t.commit_sha)err(where,'stale QA revision');
   if(['FAILED','BLOCKED','NOT_RUN'].includes(t.status)&&!safe(t.blocker))err(where,'blocker required');
   if(t.status!=='VERIFIED_PASS'&&!safe(t.next_action))err(where,'next action required');
  }
  if(new Set(ids).size!==ids.length)err(loc,'duplicate task ID');
  out.per_repository.push({repo:p.repo,task_limit:p.requested_tasks,attempted,native_claims:native,
   remaining:p.requested_tasks-native,checkpoint:p.checkpoint?.status||'UNKNOWN'});
  out.total_native_claims+=native;
 }
 if(new Set(seen).size!==seen.length)err('projects','duplicate repo/ledger');
 out.valid=errors.length===0;return out;
}
