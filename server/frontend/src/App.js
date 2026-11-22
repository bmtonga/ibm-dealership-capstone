import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";
import Register from "./components/Register/Register";
import Dealers from "./components/Dealers/Dealers";
import Dealer from "./components/Dealers/Dealer";
import PostReview from "./components/Dealers/PostReview";
import Header from "./components/Header/Header";

const Home = () => <><Header/><main style={{maxWidth:900,margin:'40px auto',textAlign:'center'}}><h1>Welcome to Dealerships</h1><img src="/static/car_dealership.jpg" alt="Car dealership" style={{maxWidth:'100%',borderRadius:12}}/><p><a className="btn btn-info m-3" href="/dealers">View Dealerships</a></p></main></>;
const About = () => <><Header/><main className="container py-5"><h1>About Us</h1><p>We connect drivers with trusted dealerships and transparent customer reviews across the United States.</p></main></>;
const Contact = () => <><Header/><main className="container py-5"><h1>Contact Us</h1><p>Email: support@dealerships.example</p></main></>;

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dealers" element={<Dealers />} />
      <Route path="/dealer/:id" element={<Dealer />} />
      <Route path="/postreview/:id" element={<PostReview />} />
      <Route path="/about" element={<About />} />
      <Route path="/contact" element={<Contact />} />
      <Route path="*" element={<Home />} />
    </Routes>
  );
}
export default App;
