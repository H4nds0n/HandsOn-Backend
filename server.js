import express from 'express'

const app = express()

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