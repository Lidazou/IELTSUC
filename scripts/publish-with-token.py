import base64,hashlib,json,pathlib,subprocess,sys,time,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parents[1]
REPO='Lidazou/IELTSUC';API='https://api.github.com';RESULT=ROOT.parent/'IELTSUC/tmp/publish-result.json'
TOKEN=sys.stdin.readline().strip()
if not TOKEN:raise SystemExit('Token input was empty.')
def api(method,path,data=None,raw=None):
 url=path if path.startswith('https://') else API+'/repos/'+REPO+path
 from urllib.parse import urlparse
 if urlparse(url).hostname not in ('api.github.com','uploads.github.com'):raise RuntimeError('Unexpected upload host.')
 headers={'Authorization':'Bearer '+TOKEN,'Accept':'application/vnd.github+json','User-Agent':'IELTSUC-publisher','X-GitHub-Api-Version':'2022-11-28'}
 body=raw if raw is not None else (json.dumps(data).encode() if data is not None else None)
 if body is not None:headers['Content-Type']='application/octet-stream' if raw is not None else 'application/json'
 req=urllib.request.Request(url,data=body,headers=headers,method=method)
 try:
  with urllib.request.urlopen(req,timeout=1200 if raw is not None else 60) as res:return json.load(res)
 except urllib.error.HTTPError as e:
  if e.code==404 and method=='GET':return None
  raise RuntimeError('GitHub returned HTTP '+str(e.code)+' for '+method+' '+url.split('?')[0]) from None
 except (OSError,TimeoutError):raise RuntimeError('Network request failed. Check connectivity to api.github.com / uploads.github.com.') from None
def publish():
 exe=ROOT/'dist/IELTSUC-1.3.1-win-x64.exe'
 if not exe.exists():raise RuntimeError('Windows EXE is missing.')
 print('Verifying repository access...',flush=True)
 repo=api('GET','')
 if not repo:raise RuntimeError('Repository access unavailable.')
 head=api('GET','/git/ref/heads/main')['object']['sha']
 base=api('GET','/git/commits/'+head)['tree']['sha']
 files=subprocess.check_output(['git','-c','safe.directory='+ROOT.as_posix(),'ls-files','-z'],cwd=ROOT).decode().strip('\0').split('\0')
 if any(p.lower().endswith(('.sqlite','.pdf','.mp3','.bak')) or p.startswith(('node_modules/','dist/')) for p in files):raise RuntimeError('Unexpected private or generated files in source manifest.')
 entries=[]
 for p in files:
  content=(ROOT/p).read_bytes();entry={'path':p,'mode':'100644','type':'blob'}
  if p.lower().endswith(('.png','.ico','.traineddata')):
   blob=api('POST','/git/blobs',{'content':base64.b64encode(content).decode(),'encoding':'base64'});entry['sha']=blob['sha']
  else:entry['content']=content.decode('utf-8-sig')
  entries.append(entry)
 print('Uploading source tree...',flush=True)
 tree=api('POST','/git/trees',{'base_tree':base,'tree':entries})
 commit=api('POST','/git/commits',{'message':'Publish IELTSUC 1.3.1 with illustrated documentation','tree':tree['sha'],'parents':[head]})
 api('PATCH','/git/refs/heads/main',{'sha':commit['sha'],'force':False})
 print('Source uploaded. Preparing release...',flush=True)
 release=api('GET','/releases/tags/v1.3.1')
 if not release:release=api('POST','/releases',{'tag_name':'v1.3.1','target_commitish':commit['sha'],'name':'IELTSUC 1.3.1 - Windows public edition','body':(ROOT/'docs/RELEASE.md').read_text('utf-8-sig'),'draft':False,'prerelease':False})
 checksum=ROOT/'dist/SHA256SUMS.txt';checksum.write_text(hashlib.sha256(exe.read_bytes()).hexdigest()+'  '+exe.name+'\n','ascii')
 assets=[exe,checksum,*[ROOT/'docs'/x for x in ['DEPLOYMENT.md','VOCABULARY.md','OLLAMA.md']],ROOT/'THIRD_PARTY_NOTICES.md']
 existing={a['name']:a for a in api('GET','/releases/'+str(release['id'])+'/assets')}
 from urllib.parse import quote
 for file in assets:
  content=file.read_bytes();digest='sha256:'+hashlib.sha256(content).hexdigest()
  if file.name in existing:
   if existing[file.name].get('digest')==digest:continue
   raise RuntimeError('Release asset already exists with different content: '+file.name)
  print('Uploading '+file.name+' ('+str(len(content))+' bytes)...',flush=True)
  api('POST',release['upload_url'].split('{')[0]+'?name='+quote(file.name),raw=content)
 final=api('GET','/releases/tags/v1.3.1')
 names={a['name'] for a in final['assets']}
 if not all(f.name in names for f in assets):raise RuntimeError('Release asset verification failed.')
 result={'published':True,'repository':repo['html_url'],'release':final['html_url'],'commit':commit['sha'],'assets':[a['name'] for a in final['assets']]}
 RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps(result,indent=2),'utf8')
 print('Published: '+final['html_url'],flush=True)
try:publish()
except Exception as e:
 RESULT.parent.mkdir(parents=True,exist_ok=True);RESULT.write_text(json.dumps({'published':False,'error':str(e)},indent=2),'utf8');print('Publication stopped: '+str(e));sys.exit(1)
finally:TOKEN=''
