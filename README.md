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
   * doc_type: required. Optional values: "TD1", "TD2", "TD3", "MRVA", "MRVB"
   * random: pass "true" to generate a random MRZ
   * country
   * surname
   * given_names
   * document_number
   * nationality
   * birth_date
   * sex
   * expiry_date
   * optional1
   * optional2
* Response:
    
    ```json
    {
        "MRZ": "Generated MRZ String",
        "surname": "random surname",
        "nationality": "random nationality",
        "sex": "random sex",
        "document_number": "random document number",
        "birth_date": "random birth date",
        "expiry_date": "random expiry date"
    }
    ```
    
    The random values only exist in random mode.
    
Sample requests:

```
/code?doc_type=TD2&random=true

/code?doc_type=TD2&country=GBR&surname=PHUONG&given_names=STEVE&document_number=FPOGDULZU&nationality=GBR&birth_date=520608&sex=M&expiry_date=311205&optional1=&optional2=
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

