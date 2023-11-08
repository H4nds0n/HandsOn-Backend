import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
const app = express()

// const encoding = 'multipart/form-data'
const encoding = 'multipart/form-data'
let counter = 0

app.use(cors())
app.use(bodyParser.raw({ type: encoding, limit: "50mb" }));
app.use(bodyParser.urlencoded({extended: true, limit: "50mb"}))
// multipart/form-data

app.post('/streaming', async (req, res) => {
    console.log(`Number requests: ${counter}`)
    const buffer = req.body
    const dataURI = `data:${encoding};base64,${buffer.toString('base64')}`;
    const data = {"base64Img": dataURI}

    const letter = await fetch("http://localhost:5001", {
        "method": "POST",
        "headers": {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        "body": JSON.stringify(data)
    }).then(response => response.json())
    console.log(letter)

    // res.status(200)
    // Testing:
    console.log(JSON.stringify(letter))
    res.status(200).send(JSON.stringify(letter))
    counter++
})

app.listen(5000, () => {
    console.log("Server listening on port 5000...");
})