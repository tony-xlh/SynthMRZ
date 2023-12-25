# SynthMRZ

Code for generating synthetic MRZ images

* gen.py: generate synthetic MRZ images based on template passport images.
* index.py: a web interface for generating MRZ strings or MRZ images.

## Installation

```
pip install -r requirements.txt
```

## APIs

### Generate MRZ String

* Endpoint: `/code`
* Methods: `GET`, `POST`
* Arguments:
   * doc_type: "TD1", "TD2", "TD3"
* Response:
    
    ```json
    {
        "MRZ": "Generated MRZ String"
    }
    ```

### Generate MRZ Image

* Endpoint: `/image`
* Methods: `GET`, `POST`
* Arguments: null, generate TD3 by default
* Response:
    
    ```json
    {
        "MRZ": "Generated MRZ String",
        "base64": "based-encoded image"
    }
    ```

