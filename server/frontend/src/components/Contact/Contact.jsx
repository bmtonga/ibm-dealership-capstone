import React, { useState } from "react";
import Header from "../Header/Header";

const initial = { first_name: "", last_name: "", email: "", message: "" };

export default function Contact() {
  const [form, setForm] = useState(initial);
  const [state, setState] = useState({
    busy: false,
    message: "",
    error: false,
  });
  const change = (event) =>
    setForm({ ...form, [event.target.name]: event.target.value });
  const submit = async (event) => {
    event.preventDefault();
    setState({ busy: true, message: "", error: false });
    try {
      const response = await fetch("/djangoapp/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await response.json();
      if (!response.ok)
        throw new Error(data.message || "Message could not be sent.");
      setForm(initial);
      setState({ busy: false, message: data.message, error: false });
    } catch (error) {
      setState({ busy: false, message: error.message, error: true });
    }
  };
  return (
    <>
      <Header />
      <main>
        <section className="page-hero compact shell">
          <span className="eyebrow">Contact us</span>
          <h1>
            Let's start a<br />
            <em>conversation.</em>
          </h1>
          <p>
            Have a question about a dealer or your account? Our team is ready to
            help.
          </p>
        </section>
        <section className="contact-grid shell">
          <div className="contact-aside">
            <h3>Talk to our team</h3>
            <p>
              Have questions or want to schedule a test drive? Call, email, or
              visit us. We usually respond within one business day.
            </p>
            <div className="contact-details-list">
              <div>
                <small>Email address</small>
                <a href="mailto:support@bestcars.com">
                  support@bestcars.com
                </a>
              </div>
              <div>
                <small>Phone number</small>
                <a href="tel:+11234567890">+1 (123) 456-7890</a>
                <span>Call to schedule a test drive</span>
              </div>
              <div>
                <small>Our dealership</small>
                <a
                  href="https://www.google.com/maps/search/?api=1&query=123+Main+Street%2C+City%2C+Country"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  123 Main Street, City, Country
                </a>
              </div>
            </div>
            <span className="contact-hours">Mon–Fri · 8:00–17:00</span>
          </div>
          <form className="form-card" onSubmit={submit}>
            <div className="field-row">
              <label>
                First name
                <input
                  name="first_name"
                  required
                  placeholder="Your first name"
                  value={form.first_name}
                  onChange={change}
                />
              </label>
              <label>
                Last name
                <input
                  name="last_name"
                  required
                  placeholder="Your last name"
                  value={form.last_name}
                  onChange={change}
                />
              </label>
            </div>
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
              How can we help?
              <textarea
                name="message"
                rows="5"
                required
                placeholder="Tell us a little about your question..."
                value={form.message}
                onChange={change}
              />
            </label>
            {state.message && (
              <p
                className={state.error ? "form-status error" : "form-status"}
                role="status"
              >
                {state.message}
              </p>
            )}
            <button
              className="button button-primary"
              type="submit"
              disabled={state.busy}
            >
          {state.busy ? "Sending..." : "Send message"}
            </button>
          </form>
        </section>
      </main>
      <Footer />
    </>
  );
}

function Footer() {
  return (
    <footer>
      <div className="shell footer-inner">
        <a className="brand footer-brand" href="/">
          <span className="brand-mark">C</span>
          <span>carwise</span>
        </a>
        <p>Better dealership decisions, powered by real drivers.</p>
        <div className="footer-links">
          <a href="/dealers">Dealers</a>
          <a href="/about">About</a>
          <a href="/contact">Contact</a>
        </div>
        <span className="copyright">© 2026 Carwise</span>
      </div>
    </footer>
  );
}
