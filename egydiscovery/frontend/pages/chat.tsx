import { useState, useEffect } from 'react';
function token(){ if(typeof window==='undefined') return ''; return localStorage.getItem('token') || ''; }
export default function Chat(){
  const [session,setSession]=useState<string>('sess-'+Math.random().toString(36).slice(2));
  const [text,setText]=useState('Hello');
  const [log,setLog]=useState<string[]>([]);

  useEffect(()=>{
    fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/v1/events/chat`,{
      method:'POST', headers:{'Content-Type':'application/json','Authorization':'Bearer '+token()},
      body: JSON.stringify({session_id:session,event_type:'start',text:''})
    });
  },[]);

  async function send(){
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/v1/events/chat`,{
      method:'POST', headers:{'Content-Type':'application/json','Authorization':'Bearer '+token()},
      body: JSON.stringify({session_id:session,event_type:'message',text})
    }); setLog([...log, 'You: '+text, 'Sent to automation']);
    setText('');
  }

  return (<main style={{padding:24,maxWidth:720,margin:'0 auto',fontFamily:'system-ui'}}>
    <h1>Chatbot (event-driven)</h1>
    <div style={{border:'1px solid #ddd',padding:12,minHeight:200,marginBottom:12}}>{log.map((l,i)=><div key={i}>{l}</div>)}</div>
    <input value={text} onChange={e=>setText(e.target.value)} style={{width:'100%',padding:10,marginBottom:8}}/>
    <button onClick={send}>Send</button>
  </main>)
}
