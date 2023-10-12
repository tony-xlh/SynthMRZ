import names
import random
import datetime
import mrz.generator.td1
import mrz.generator.td2
import mrz.generator.td3
import mrz.generator.mrva
import mrz.generator.mrvb
from PIL import Image
from trdg.generators import GeneratorFromStrings

VALID_COUNTRY_CODES = ['USA', 'CAN', 'GBR', 'AUS', 'FRA', 'CHN', 'IND',
                       'BRA', 'JPN', 'ZAF', 'RUS', 'MEX', 'ITA', 'ESP', 'NLD', 'SWE', 'ARG', 'BEL', 'CHE']

MRZ_TYPES = ['TD1','TD2','TD3','MRVA','MRVB']

def random_generate(doc_type=""):
    surname = random_surname()
    given_names = random_given_names()
    nationality = random.choice(VALID_COUNTRY_CODES)
    sex = random.choice(['M', 'F'])
    if doc_type == "" or doc_type == None:
        doc_type = random.choice(MRZ_TYPES)
    document_number = random_string(9, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    birth_date = random_date().strftime('%y%m%d')
    expiry_date = random_date(start_year=datetime.datetime.now(
    ).year, end_year=datetime.datetime.now().year + 10).strftime('%y%m%d')
    code = generate_MRZ(doc_type,nationality,surname,given_names,document_number,nationality,birth_date,sex,expiry_date,"","")
    return code

def generate_images(code):
    fonts = ["OCR-B.ttf"]
    lines = str(code).split("\n")
    generator = GeneratorFromStrings(lines,count = len(lines),fonts = fonts)
    imgs = []
    for img, lbl in generator:
        imgs.append(img)
    return imgs

def random_string(length=10, allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

def random_surname():
    return names.get_last_name()

def random_given_names():
    return names.get_first_name()

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
    dst = Image.new('RGB', (w, h))
    top = 0
    for img in imgs:
        dst.paste(img, (0, top))
        top = top + img.height
    return dst


if __name__ == "__main__":
    code = random_generate()
    imgs = generate_images(code)
    merged = merged_image(imgs)
    merged.save("out.jpg")
    