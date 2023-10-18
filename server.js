import express from 'express'
import cors from 'cors'
import bodyParser from 'body-parser'
import multer from 'multer'

const app = express()

const encoding = 'image/jpeg'
const storage = multer.memoryStorage();
const upload = multer({storage: storage})

app.use(cors())
app.use(bodyParser.raw({ type: encoding, limit: "50mb" }));
app.use(bodyParser.urlencoded({extended: true, limit: "50mb"}))
// multipart/form-data


app.get('/', (req, res) => {
    res.send("Hell, World!")
})

app.post('/streaming', upload.single('blobData'), (req, res) => {
    console.log(req)
    const buffer = req.body
    // const b = new Blob([req.body], {type: "image/jpg"})
    const dataURI = `data:${encoding};base64,${buffer.toString('base64')}`;
    res.status(200).send(`<img src="${dataURI}">`)
})

app.listen(5000, () => {
    console.log("Server listening on port 5000...");
})