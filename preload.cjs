const {contextBridge,ipcRenderer}=require('electron');
const allowed=['pronunciation','openResource','openGrammarVideo','state','settings','models','words','deleteWord','import','start','pause','tick','question','ai','parseExam','saveExam','submit','note','backup','restore'];
contextBridge.exposeInMainWorld('api',{call:async(name,data)=>{if(!allowed.includes(name))throw Error('未知操作');let r=await ipcRenderer.invoke(name,data);if(!r.ok)throw Error(r.error);return r.data},onOCR:cb=>ipcRenderer.on('ocr-progress',(_,m)=>cb(m))});
