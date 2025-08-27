import { useEffect } from 'react';
export default function OAuthComplete(){
  useEffect(()=>{
    if(typeof window !== 'undefined'){
      const hash = new URLSearchParams(window.location.hash.slice(1));
      const token = hash.get('token');
      if(token){ localStorage.setItem('token', token); window.location.href = '/dashboard'; }
      else { window.location.href = '/login'; }
    }
  },[]);
  return null;
}
