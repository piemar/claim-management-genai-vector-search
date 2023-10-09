
# Car Insurance Claim management 
The claim adjustment procedure can be lengthy and susceptible to mistakes. A client from the insurance sector recently shared, “Every time an adjuster gets involved, it costs us.” For every claim, adjusters must sift through the client's prior claims and associated guidelines. These records are often dispersed over various systems and formats, complicating the retrieval of pertinent data and delaying the generation of an accurate payment estimate.

Using a vector database, the adjuster can easily request the AI to "display images resembling this collision." The system, powered by Vector Search, then provides photos of vehicular accidents with matching damage patterns from the claims history. This allows the adjuster to swiftly juxtapose the accident photos with the most pertinent ones from the insurer's claim archives.

This application ix trying to showcase the above. STILL WIP

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
Create Atlas Search index, on database insurance_company and collection images using the JSON config and lappy below config
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
            "captionEncodings": {
                "dimensions": 128,
                "similarity": "euclidean",
                "type": "knnVector"
            }            
        }
    }
}
```

### Set up and start the Beckend 

Navigate to the frontend directory and install the required npm packages:

```sh
python3.11 app.py --server 
```
### Set up and start the Frontend 

Navigate to the frontend directory and install the required npm packages:

```sh
cd claim-management-frontend
npm install
npm start
```

The React application should now be running on [http://localhost:3000](http://localhost:3000), and the Flask application should be running on [http://localhost:5000](http://localhost:5000).

### Using the Application

1. Open your web browser and navigate to [http://localhost:3000](http://localhost:3000).
2. Click the choose file button to select a picture to upload match against reported claims 
3. The application will encode the image and interact with the backend to retrieve related similar claims

