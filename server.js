import express from 'express'
import cors from 'cors'

const app = express()

app.use(cors())
app.use(express.json())

app.get('/', (req, res) => {
    res.send("Hell, World!")
})

app.post('/streaming', (req, res) => {
    console.log("Blob: ", req.body)
    res.send(200, "Successful")
})

app.listen(5000, () => {
    console.log("Server listening on port 5000...");
})