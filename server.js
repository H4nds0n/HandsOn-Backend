import express from "express";
import cors from "cors";
import bodyParser from "body-parser";

const app = express();

// const encoding = 'multipart/form-data'
const encoding = "image/jpeg";
let counter = 0;
let executionTimes = [];

app.use(cors());
app.use(express.json())
app.use(bodyParser.raw({ type: encoding, limit: "50mb" }));
app.use(bodyParser.urlencoded({ extended: true, limit: "50mb" }));
// multipart/form-data

app.post("/streaming", async (req, res) => {
  console.log(`Number requests: ${counter}`);
  if (Object.keys(req.body).length != 0) {
    const data = { base64Img: req.body.img };


    let before = Date.now();
    const letter = await fetch("http://localhost:5001", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }).then((response) => response.json());
    let after = Date.now();
    console.log("Executiontime in ms:", after - before);
    executionTimes.push(after - before);
    let sum = 0;
    executionTimes.forEach((i) => {
      sum += i;
    });
    console.log("Average [ms]: ", sum / executionTimes.length);
    console.log(letter);
    // res.status(200)
    // Testing:
    res.status(200).send(JSON.stringify(letter));
    counter++;
  }
});

app.use("/*", (req, res) => {
  res
    .status(404)
    .send(
      '<h1>Nothing here, bro...</h1><br><img src="https://media1.giphy.com/media/BcuLq7kvQWuftTzBh4/giphy.gif?cid=6c09b9526kc17zmhlrwvbq3u2y0ncaz0igfn49x4zx7arwar&ep=v1_stickers_related&rid=giphy.gif&ct=s"/>'
    );
});

app.listen(5000, () => {
  console.log("Server listening on port 5000...");
});
