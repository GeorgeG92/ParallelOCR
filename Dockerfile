FROM kkwok/docker-python3-opencv-poppler

RUN pip install --upgrade pip

# install tesseract
RUN apt-get update && apt install -y tesseract-ocr

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./src ./src
