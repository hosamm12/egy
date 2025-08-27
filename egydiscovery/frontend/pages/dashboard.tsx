import { useState } from 'react';
export default function Dashboard(){
  const [prompt, setPrompt] = useState('Find 5 public leads in Hurghada and score them'); const [out, setOut] = useState('—');
  function token(){ if(typeof window==='undefined') return ''; return localStorage.getItem('token') || ''; }
  async function call(path){
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/v1/agents/${path}`, { method:'POST', headers:{'Content-Type':'application/json','Authorization':'Bearer '+token()}, body: JSON.stringify({prompt}) });
    const data = await res.json(); setOut(JSON.stringify(data,null,2));
  }
  return (<main style={{padding:24,maxWidth:900,margin:'0 auto',fontFamily:'system-ui'}}>
    <h1>Master Agent Control</h1>
    <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} style={{width:'100%',minHeight:160}}/>
    <div style={{margin:'8px 0'}}>
      <button onClick={()=>call('master')} style={{marginRight:8}}>Run Master</button>
      <button onClick={()=>call('route')}>Run Route</button>
    </div>
    <pre style={{background:'#0b1020',color:'#b7c7ff',padding:16,borderRadius:12}}>{String(out)}</pre>
  </main>)
}
