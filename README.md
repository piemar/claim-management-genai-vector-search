
# Getting started
### Update config.ini file
Updated URI with your appropriate credentials

```sh
[MongoDB]
URI = mongodb+srv://user:password@<cluster_name>.tcrpd.mongodb.net/?retryWrites=true&w=majority
DATABASE = insurance_company
COLLECTION = images
```

### Encode images and store vectors in MongoDB Atlas
Will install python requirements and run python application to encode images located in images folder

```sh
pip install git+https://github.com/huggingface/transformers 
pip install -r req.txt
python3.11 app.py --path images              
```

### Create Atlas Search Index
Create Atlas Search index, on database starwars and collection characters using the JSON config and lappy below config
```json
{
    "mappings": {
        "dynamic": true,
        "fields": {
            "imageEncodings": {
                "dimensions": 128,
                "similarity": "euclidean",
                "type": "knnVector"
            },
            "textEncodings": {
                "dimensions": 128,
                "similarity": "euclidean",
                "type": "knnVector"
            }            
        }
    }
}
```


### Set up and start the Frontend 

Navigate to the frontend directory and install the required npm packages:

```sh
cd starwars-frontend
npm install
npm start
```

The React application should now be running on [http://localhost:3000](http://localhost:3000), and the Flask application should be running on [http://localhost:5000](http://localhost:5000).

### Using the Application

1. Open your web browser and navigate to [http://localhost:3000](http://localhost:3000).
2. Click the choose file button to select a selfie picture to match against Starwars characters
3. The application will encode the selfie and interact with the backend to retrieve related Star Wars characters.

