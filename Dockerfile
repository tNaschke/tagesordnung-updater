FROM python:3

WORKDIR /usr/src/app
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY page.html ./
COPY page.en.html ./

COPY to_update.py ./
CMD ["python", "./to_update.py"]
