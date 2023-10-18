import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'

const app = express()

app.use(cors())
app.use(bodyParser.raw({ type: 'image/png' }));
// app.use(bodyParser.json())


app.get('/', (req, res) => {
    res.send("Hell, World!")
})

app.post('/streaming', (req, res) => {
    const buffer = req.body
    // const b = new Blob([req.body], {type: "image/jpg"})
    const dataURI = `data:image/png;base64,${buffer.toString('base64')}`;
    res.status(200).send('success')
    console.log(req.body)
})

app.listen(5000, () => {
    console.log("Server listening on port 5000...");
})