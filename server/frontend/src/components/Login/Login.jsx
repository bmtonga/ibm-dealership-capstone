import React, { useState } from "react";
import Header from "../Header/Header";

export default function Login(){
  const [userName,setUserName]=useState(""),[password,setPassword]=useState("");
  const [state,setState]=useState({busy:false,error:""});
  const submit=async e=>{
    e.preventDefault(); setState({busy:true,error:""});
    try{
      const response=await fetch("/djangoapp/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({userName,password})});
      const data=await response.json();
      if(!response.ok) throw new Error(data.message||"The username or password is incorrect.");
      sessionStorage.setItem("username",data.userName);
      sessionStorage.setItem("firstname",data.firstName||"");
      sessionStorage.setItem("lastname",data.lastName||"");
      window.location.href="/dealers";
    }catch(error){setState({busy:false,error:error.message})}
  };
  return <><Header/><main className="auth-page"><div className="auth-shell"><aside className="auth-aside"><div><span className="eyebrow light">Welcome back</span><h2>Good decisions start with real experiences.</h2><p>Sign in to share reviews and help drivers find dealerships they can trust.</p></div><small>Carwise · The confident way to choose</small></aside><form className="auth-form" onSubmit={submit}><h1>Sign in</h1><p>Welcome back. Enter your details below.</p><label>Username<input autoComplete="username" required placeholder="Enter your username" value={userName} onChange={e=>setUserName(e.target.value)}/></label><label>Password<input autoComplete="current-password" type="password" required placeholder="Enter your password" value={password} onChange={e=>setPassword(e.target.value)}/></label>{state.error&&<p className="form-status error" role="alert">{state.error}</p>}<button className="button button-primary" disabled={state.busy}>{state.busy?"Signing in...":"Sign in →"}</button><div className="auth-switch">New to Carwise? <a href="/register">Create an account</a></div></form></div></main></>;
}
