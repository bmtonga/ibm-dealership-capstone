import React, { useState } from "react";
export default function Header() {
  const [open, setOpen] = useState(false);
  const username = sessionStorage.getItem("username");
  const logout = async (e) => {
    e.preventDefault();
    const r = await fetch("/djangoapp/logout");
    if (await r.json()) {
      sessionStorage.clear();
      window.location.href = "/";
    }
  };
  return (
    <header className="site-header">
      <div className="shell nav-wrap">
        <a className="brand" href="/">
          <span className="brand-mark">C</span>
          <span>carwise</span>
        </a>
        <button
          className="menu-toggle"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? "×" : "☰"}
        </button>
        <nav className={open ? "nav-links open" : "nav-links"}>
          <a href="/dealers">Dealers</a>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
        </nav>
        <div className="nav-actions">
          {username ? (
            <>
              <span className="user-chip">
                <span>{username.charAt(0).toUpperCase()}</span>
                {username}
              </span>
              <a href="/djangoapp/logout" onClick={logout}>
                Log out
              </a>
            </>
          ) : (
            <>
              <a href="/login">Log in</a>
              <a className="button button-small button-dark" href="/register">
              Get started
              </a>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
