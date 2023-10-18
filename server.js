import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
const app = express()

const encoding = 'multipart/form-data'
let counter = 0

app.use(cors())
app.use(bodyParser.raw({ type: encoding, limit: "50mb" }));
app.use(bodyParser.urlencoded({extended: true, limit: "50mb"}))
// multipart/form-data


app.get('/', (req, res) => {
    res.send("Hell, World!")
})

app.post('/streaming', (req, res) => {
    console.log(`Number requests: ${counter}`)
    const buffer = req.body
    const dataURI = `data:${encoding};base64,${buffer.toString('base64')}`;
    // res.status(200)
    // Testing:
    res.status(200).send(`<img src="${dataURI}">`)
    counter++
})

app.listen(5000, () => {
    console.log("Server listening on port 5000...");
})