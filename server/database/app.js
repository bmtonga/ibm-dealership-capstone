const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const  cors = require('cors')
const app = express()
const port = process.env.PORT || 3030;

app.use(cors({ origin: process.env.CORS_ORIGIN || true }));
app.use(express.json({ limit: '100kb' }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

const useMongo = Boolean(process.env.MONGODB_URI);


const Reviews = require('./review');

const Dealerships = require('./dealership');

async function seedDatabase() {
  if (await Reviews.countDocuments() === 0) await Reviews.insertMany(reviews_data.reviews);
  if (await Dealerships.countDocuments() === 0) await Dealerships.insertMany(dealerships_data.dealerships);
}
const memoryReviews = reviews_data.reviews.map((item) => ({ ...item }));
const memoryDealers = dealerships_data.dealerships.map((item) => ({ ...item }));
if (useMongo) {
  mongoose.connect(process.env.MONGODB_URI);
  mongoose.connection.once('open', () => seedDatabase().catch(console.error));
}


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = useMongo ? await Reviews.find() : memoryReviews;
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const id = Number.parseInt(req.params.id, 10);
    const documents = useMongo ? await Reviews.find({dealership: id}) : memoryReviews.filter((review) => review.dealership === id);
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    res.json(useMongo ? await Dealerships.find().sort({ id: 1 }) : memoryDealers);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const query = state.toLowerCase() === 'all' ? {} : { state: new RegExp(`^${escapeRegExp(state)}$`, 'i') };
    const documents = useMongo ? await Dealerships.find(query).sort({ id: 1 }) :
      memoryDealers.filter((dealer) => !Object.keys(query).length || dealer.state.toLowerCase() === state.toLowerCase());
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = Number.parseInt(req.params.id, 10);
    if (!Number.isInteger(id)) return res.status(400).json({ error: 'Invalid dealer id' });
    const dealer = useMongo ? await Dealerships.findOne({ id }) : memoryDealers.find((item) => item.id === id);
    return dealer ? res.json([dealer]) : res.status(404).json({ error: 'Dealer not found' });
  } catch (error) {
    res.status(500).json({ error: 'Error fetching dealership' });
  }
});

//Express route to insert review
app.post('/insert_review', async (req, res) => {
  const data = req.body;
  const required = ['name', 'dealership', 'review', 'purchase_date', 'car_make', 'car_model', 'car_year'];
  if (required.some((field) => data[field] === undefined || data[field] === '')) {
    return res.status(400).json({ error: 'Missing required review fields' });
  }
  const documents = useMongo ? await Reviews.find().sort({ id: -1 }) : [...memoryReviews].sort((a, b) => b.id - a.id);
  let new_id = documents.length ? documents[0].id + 1 : 1;

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = useMongo ? await review.save() : { ...review.toObject(), _id: undefined };
    if (!useMongo) memoryReviews.push(savedReview);
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.get('/health', (req, res) => res.json({ status: 'ok', storage: useMongo ? 'mongodb' : 'memory' }));

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
