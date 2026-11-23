import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Header from "../Header/Header";
import positive from "../assets/positive.png";
import neutral from "../assets/neutral.png";
import negative from "../assets/negative.png";
import "./Dealers.css";
export default function Dealer() {
  const { id } = useParams(),
    [dealer, setDealer] = useState({}),
    [reviews, setReviews] = useState([]),
    [loaded, setLoaded] = useState(false);
  useEffect(() => {
    Promise.all([
      fetch(`/djangoapp/dealer/${id}`).then((r) => r.json()),
      fetch(`/djangoapp/reviews/dealer/${id}`).then((r) => r.json()),
    ])
      .then(([d, r]) => {
        if (d.status === 200) setDealer(Array.from(d.dealer)[0] || {});
        if (r.status === 200) setReviews(r.reviews || []);
      })
      .finally(() => setLoaded(true));
  }, [id]);
  const icon = (s) =>
    s === "positive" ? positive : s === "negative" ? negative : neutral;
  return (
    <>
      <Header />
      <main className="dealer-detail">
        <section className="detail-head shell">
          <a className="detail-back" href="/dealers">
          Back to all dealerships
          </a>
          <div className="detail-title-row">
            <div>
              <span className="eyebrow">Verified dealership</span>
              <h1>{dealer.full_name || "Loading dealership..."}</h1>
              <p>
                ⌖ {dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}
              </p>
            </div>
            {sessionStorage.getItem("username") && (
              <a className="button button-primary" href={`/postreview/${id}`}>
              Write a review
              </a>
            )}
          </div>
        </section>
        <section className="shell">
          <div className="results-head">
            <div>
              <h2>Customer experiences</h2>
              <span>{reviews.length} verified reviews</span>
            </div>
          </div>
          {!loaded ? (
            <div className="loading-state">
              <span className="loader" />
              Loading reviews...
            </div>
          ) : reviews.length ? (
            <div className="review-grid">
              {reviews.map((r, i) => (
                <article className="review-card" key={r.id || i}>
                  <div className="sentiment">
                    <img src={icon(r.sentiment)} alt="" />
                    <span>{r.sentiment || "customer review"}</span>
                  </div>
                  <p className="review-text">“{r.review}”</p>
                  <div className="reviewer">
                    <strong>{r.name}</strong>
                    {r.car_year} {r.car_make} {r.car_model}
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <h3>No reviews yet</h3>
              <p>
                Be the first customer to share an experience with this
                dealership.
              </p>
            </div>
          )}
        </section>
      </main>
    </>
  );
}
