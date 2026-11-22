import React from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";
import { csrfFetch } from '../../api';

export default function Header() {
  const username = sessionStorage.getItem('username');
  const logout = async (event) => {
    event.preventDefault();
    const response = await csrfFetch('/djangoapp/logout', { method: 'POST' });
    if (response.ok) {
      sessionStorage.clear();
      window.location.href = '/';
    }
  };
  return <nav className="navbar navbar-expand-lg navbar-light" style={{backgroundColor:'darkturquoise',minHeight:'1in'}}>
    <div className="container-fluid"><h2 className="me-5">Dealerships</h2>
      <div className="navbar-nav me-auto"><a className="nav-link" href="/">Home</a><a className="nav-link" href="/dealers">Dealers</a><a className="nav-link" href="/about">About Us</a><a className="nav-link" href="/contact">Contact Us</a></div>
      <div>{username ? <><span className="me-3">{username}</span><a href="/" onClick={logout}>Logout</a></> : <><a className="me-3" href="/login">Login</a><a href="/register">Register</a></>}</div>
    </div>
  </nav>;
}
