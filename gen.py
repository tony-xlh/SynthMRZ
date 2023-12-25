import names
import random
import json
import datetime
import mrz.generator.td1
import mrz.generator.td2
import mrz.generator.td3
import mrz.generator.mrva
import mrz.generator.mrvb
import os
from PIL import Image, ImageFont, ImageDraw

COUNTRIES = {
    "BLR":"Belarus-passport-mini.jpg",
    "BEL":"Belgium-passport-mini.jpg",
    "BGR":"Bulgaria-passport-mini.jpg",
    "CAN":"Canada-passport-mini.jpg",
    "CHL":"Chile-passport-mini.jpg",
    "CHN":"China-passport-mini.jpg",
    "DOM":"Dominicana-passport-mini.jpg",
    "EST":"Estonia-passport-mini.jpg",
    "D":"Germany-passport-mini.jpg",
    "IDN":"Indonesia-passport-mini.jpg",
    "IRL":"Ireland-passport-mini.jpg",
    "ITA":"Italy-passport-mini.jpg",
    "JPN":"Japanese-passport.jpg",
    "KAZ":"Kazakhstan-passport-mini.jpg",
    "MEX":"Mexico-passport-mini.jpg",
    "MDA":"Moldova-passport-mini.jpg",
    "NLD":"Netherlands-passport-mini.jpg",
    "POL":"Poland-passport-mini.jpg",
    "ROU":"Romania-passport-mini.jpg",
    "SVK":"Slovakia-passport-mini.jpg",
    "ESP":"Spain-passport-mini.jpg",
    "GBR":"United-kingdom-of-great-britain-passport-mini.jpg",
    "URY":"Uruguay-passport-mini.jpg",
    "UZB":"Uzbekistan-passport-mini.jpg",
    "USA":"USA-Passport.jpg"
}

MRZ_TYPES = ['TD1','TD2','TD3','MRVA','MRVB']

def random_generate(doc_type="",nationality="GBR"):
    surname = random_surname()
    given_names = random_given_names()
    if nationality == "" or nationality == None:
        nationality = random.choice(list(COUNTRIES.keys()))
    sex = random.choice(['M', 'F'])
    if doc_type == "" or doc_type == None:
        doc_type = random.choice(MRZ_TYPES)
    document_number = random_string(9, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    birth_date = random_date().strftime('%y%m%d')
    expiry_date = random_date(start_year=datetime.datetime.now(
    ).year, end_year=datetime.datetime.now().year + 10).strftime('%y%m%d')
    code = generate_MRZ(doc_type,nationality,surname,given_names,document_number,nationality,birth_date,sex,expiry_date,"","")
    return code
    
def random_generate_with_parts(doc_type="",nationality="GBR"):
    surname = random_surname()
    given_names = random_given_names()
    if nationality == "" or nationality == None:
        nationality = random.choice(list(COUNTRIES.keys()))
    sex = random.choice(['M', 'F'])
    if doc_type == "" or doc_type == None:
        doc_type = random.choice(MRZ_TYPES)
    document_number = random_string(9, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    birth_date = random_date().strftime('%y%m%d')
    expiry_date = random_date(start_year=datetime.datetime.now(
    ).year, end_year=datetime.datetime.now().year + 10).strftime('%y%m%d')
    code = generate_MRZ(doc_type,nationality,surname,given_names,document_number,nationality,birth_date,sex,expiry_date,"","")
    return {
        "MRZ": str(code),
        "surname": surname,
        "nationality": nationality,
        "sex": sex,
        "document_number": document_number,
        "birth_date": birth_date,
        "expiry_date": expiry_date
    }

def random_string(length=10, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

def random_surname():
    return names.get_last_name()

def random_given_names():
    return names.get_first_name()

def random_nationality():
    return random.choice(list(COUNTRIES.keys()))

def random_date(start_year=1900, end_year=datetime.datetime.now().year):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)

    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  # February
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):  # leap year
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)

    return datetime.date(year, month, day)

def generate_MRZ(doc_type,country,surname,given_names,document_number,nationality,birth_date,sex,expiry_date,optional1,optional2):
    code = ""
    if doc_type == "TD1":
        code = mrz.generator.td1.TD1CodeGenerator("I", country, document_number, birth_date, sex, expiry_date,nationality, surname, given_names, optional1, optional2)
    elif doc_type == "TD2":
        code = mrz.generator.td2.TD2CodeGenerator("I", country, surname, given_names, document_number, nationality, birth_date, sex, expiry_date, optional1)
    elif doc_type == "TD3":
        code = mrz.generator.td3.TD3CodeGenerator("P", country, surname, given_names, document_number, nationality, birth_date, sex, expiry_date, optional1)
    elif doc_type == "MRVA":
        code = mrz.generator.mrva.MRVACodeGenerator("V", country, surname, given_names, document_number, nationality, birth_date, sex, expiry_date, optional1)
    elif doc_type == "MRVB":
        code = mrz.generator.mrvb.MRVBCodeGenerator("V", country, surname, given_names, document_number, nationality, birth_date, sex, expiry_date, optional1)
    return code

def merged_image(imgs):
    w = imgs[0].width
    h = 0
    for img in imgs:
        h = h + img.height
    dst = Image.new('RGBA', (w, h))
    top = 0
    for img in imgs:
        dst.paste(img, (0, top))
        top = top + img.height

    datas = dst.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)
    dst.putdata(newData)
    return dst

def mrz_filled(code,nationality):
    code = str(code)
    f = open("images/1.itp","r",encoding="utf-8")
    content = f.read()
    f.close()
    project = json.loads(content)
    img_name = COUNTRIES[nationality]
    images = project["images"]
    image = images[img_name]
    boxes = image["boxes"]
    #print(boxes)
    box1 = boxes[0]
    box2 = boxes[1]
    width = box1["geometry"]["width"]
    font_size = int(width/1828*56)
    img = Image.open(os.path.join("images",img_name+"-text-removed.jpg"))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("OCRB-Regular.ttf", font_size)
    draw.text((box1["geometry"]["X"], box1["geometry"]["Y"]), code.split("\n")[0], fill ="black", font = font, align ="right")  
    draw.text((box2["geometry"]["X"], box2["geometry"]["Y"]), code.split("\n")[1], fill ="black", font = font, align ="right")  
    return img

if __name__ == "__main__":
    print("Generating...")
    for key in COUNTRIES.keys():
        if os.path.exists(key) == False:
            os.mkdir(key)
        for i in range(20):
            print(key+": "+str(i))
            code = random_generate(doc_type="TD3",nationality=key)
            full = mrz_filled(code,key)
            #full.save(key+".jpg")
            formatted_index = "{:0>2d}".format(i)
            full.save(os.path.join(key,formatted_index+".jpg"))
            f = open(os.path.join(key,formatted_index+".txt"),"w",encoding="utf8")
            f.write(str(code))
            f.close()
    