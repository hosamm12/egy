import { useState } from 'react';
export default function Login(){
  const [email, setEmail] = useState(''); const [password, setPassword] = useState('');
  async function login(){
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/api/v1/auth/login`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email,password}) });
    const data = await res.json();
    if(res.ok){ localStorage.setItem('token', data.access_token); window.location.href='/dashboard'; } else { alert(data.detail||'Login failed'); }
  }
  return (<main style={{padding:24,maxWidth:520,margin:'0 auto',fontFamily:'system-ui'}}>
    <h1>Sign in</h1>
    <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} style={{display:'block',width:'100%',padding:10,margin:'8px 0'}}/>
    <input type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} style={{display:'block',width:'100%',padding:10,margin:'8px 0'}}/>
    <button onClick={login} style={{padding:'10px 14px'}}>Sign in</button>
    <p style={{color:'#666'}}>No account? Use the API to register.</p>
  </main>)
}
