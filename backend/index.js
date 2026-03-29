// CommonJS version
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const { fileURLToPath } = require('url');
const fs = require('fs');
const app = express();
app.use(cors());

const uploadFolder = 'imagesUploaded';
// Convert images into public urls so that we can access them (this is our port and then images)
app.use('/images', express.static(uploadFolder));
if (!fs.existsSync(uploadFolder)) fs.mkdirSync(uploadFolder);

// port number server will be listening on
const PORT = 3000;

// Set up Multer storage (where and how files are stored)
const storage = multer.diskStorage({
  destination: function (req, file, cb) {           // file is what multer recieves
    cb(null, uploadFolder);        // every uploaded file goes to imagesUploaded given no errors
  },
  filename: function (req, file, cb) {
    const name = req.body.name ? req.body.name.trim() : 'no-name';
    const timeStamp = Date.now();
    const extension = path.extname(file.originalname).toLowerCase();
    const newName = `${name}-${timeStamp}${extension}`;

    cb(null, newName);
  }
});

const upload = multer({ storage: storage });           // configure multer settings


// post endpoint --> this route only listens to post requests 
// api/upload is route in backend
// the backend sees this request and executes it 
// multer expects a single file in the request under the field name image 
app.post('/api/upload', upload.single('image'), (req, res) => {   // req contains metadata about the file
  // After the file is uploaded
  if (!req.file) {
    return res.status(400).json({ error: 'No file uploaded' });   // if this isn't a file, produce a message
  }

  // req.file contains info about the uploaded file
  console.log('File saved at:', req.file.path);
  return res.status(200).json({ message: 'File uploaded successfully', path: req.file.path });
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});

// Create an API endpoint that when we call from the webpage it returns of all images we have uloaded
app.get('/api/images', (req, res) => {
  const files = fs.readdirSync(uploadFolder);     // Looks inside the folder imagesUploaded

  const imageUrls = files.map(file => ({
    name: file,
    url: `http://localhost:3000/images/${file}`
  }));

  // res is for the response sent as json back to the webpage
  res.json(imageUrls);
});