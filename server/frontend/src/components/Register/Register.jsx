import React, { useState } from 'react';
import Header from '../Header/Header';
import { csrfFetch } from '../../api';
import '../Login/Login.css';

export default function Register() {
  const [form, setForm] = useState({ userName:'', password:'', firstName:'', lastName:'', email:'' });
  const update = (event) => setForm({...form, [event.target.name]: event.target.value});
  const submit = async (event) => {
    event.preventDefault();
    const response = await csrfFetch('/djangoapp/register', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(form)});
    const result = await response.json();
    if (!response.ok) return alert(result.error || 'Registration failed');
    sessionStorage.setItem('username', result.userName);
    sessionStorage.setItem('firstname', result.firstName || '');
    sessionStorage.setItem('lastname', result.lastName || '');
    window.location.href = '/dealers';
  };
  return <><Header/><main className="container py-5"><h1>Create account</h1><form onSubmit={submit} style={{maxWidth:480}}>
    {[['userName','Username','text'],['firstName','First name','text'],['lastName','Last name','text'],['email','Email','email'],['password','Password (8+ characters)','password']].map(([name,label,type]) =>
      <label key={name} className="form-label d-block">{label}<input required={name==='userName'||name==='password'} minLength={name==='password'?8:undefined} className="form-control" name={name} type={type} onChange={update}/></label>)}
    <button className="btn btn-primary" type="submit">Register</button>
  </form></main></>;
}
