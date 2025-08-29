import { useState } from 'react';
export default function LeadForm(){
  const [form,setForm]=useState({name:'',email:'',phone:'',whatsapp:'',message:'',url:''});
  const [out,setOut]=useState<any>('—');
  async function submit(){
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/v1/events/lead`, {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({...form, source:'form', tag:'site'})
    });
    const data = await res.json(); setOut(JSON.stringify(data,null,2));
  }
  return (<main style={{padding:24,maxWidth:720,margin:'0 auto',fontFamily:'system-ui'}}>
    <h1>Lead capture form</h1>
    {['name','email','phone','whatsapp','url'].map(k=> <input key={k} placeholder={k} value={(form as any)[k]} onChange={e=>setForm({...form,[k]:e.target.value})} style={{display:'block',width:'100%',padding:10,margin:'8px 0'}}/>)}
    <textarea placeholder="message" value={form.message} onChange={e=>setForm({...form,message:e.target.value})} style={{width:'100%',minHeight:120}}/>
    <button onClick={submit} style={{padding:'10px 14px'}}>Submit</button>
    <pre style={{background:'#0b1020',color:'#b7c7ff',padding:16,borderRadius:12}}>{String(out)}</pre>
  </main>)
}
