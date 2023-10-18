import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'

const app = express()

app.use(cors())
// app.use(express.json())
app.use(bodyParser.json())

app.get('/', (req, res) => {
    res.send("Hell, World!")
})

app.post('/streaming', (req, res) => {
    console.log("Blob: ", req.body)
    res.status(200).send(`<img src="${req.body}"></img>`)
})

app.listen(5000, () => {
    console.log("Server listening on port 5000...");
})