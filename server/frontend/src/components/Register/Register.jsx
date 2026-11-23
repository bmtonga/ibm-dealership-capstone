import React, { useState } from "react";
import Header from "../Header/Header";

export default function Register() {
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    userName: "",
    email: "",
    password: "",
  });
  const [state, setState] = useState({ busy: false, error: "" });
  const change = (e) => setForm({ ...form, [e.target.name]: e.target.value });
  const submit = async (e) => {
    e.preventDefault();
    setState({ busy: true, error: "" });
    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      if (!response.ok)
        throw new Error(data.message || "Account could not be created.");
      sessionStorage.setItem("username", data.userName);
      sessionStorage.setItem("firstname", data.firstName || form.firstName);
      sessionStorage.setItem("lastname", data.lastName || form.lastName);
      window.location.href = "/dealers";
    } catch (error) {
      setState({ busy: false, error: error.message });
    }
  };
  return (
    <>
      <Header />
      <main className="auth-page">
        <div className="auth-shell">
          <aside className="auth-aside">
            <div>
              <span className="eyebrow light">Join the community</span>
              <h2>Your experience can move someone forward.</h2>
              <p>
                Create an account to post dealership reviews and help other
                drivers choose confidently.
              </p>
            </div>
            <small>Clear. Helpful. Community-powered.</small>
          </aside>
          <form className="auth-form" onSubmit={submit}>
            <h1>Create account</h1>
            <p>It only takes a minute to get started.</p>
            <div className="form-name-row">
              <label>
                First name
                <input
                  name="firstName"
                  required
                  placeholder="First name"
                  value={form.firstName}
                  onChange={change}
                />
              </label>
              <label>
                Last name
                <input
                  name="lastName"
                  required
                  placeholder="Last name"
                  value={form.lastName}
                  onChange={change}
                />
              </label>
            </div>
            <label>
              Username
              <input
                name="userName"
                required
                placeholder="Choose a username"
                value={form.userName}
                onChange={change}
              />
            </label>
            <label>
              Email address
              <input
                name="email"
                type="email"
                required
                placeholder="you@example.com"
                value={form.email}
                onChange={change}
              />
            </label>
            <label>
              Password
              <input
                name="password"
                type="password"
                minLength="8"
                required
                placeholder="At least 8 characters"
                value={form.password}
                onChange={change}
              />
            </label>
            {state.error && (
              <p className="form-status error" role="alert">
                {state.error}
              </p>
            )}
            <button className="button button-primary" disabled={state.busy}>
          {state.busy ? "Creating account..." : "Create account"}
            </button>
            <div className="auth-switch">
              Already a member? <a href="/login">Sign in</a>
            </div>
          </form>
        </div>
      </main>
    </>
  );
}
