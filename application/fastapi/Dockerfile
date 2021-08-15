FROM python:3.7
COPY requirements.txt ./fastapi/requirements.txt
RUN pip3 install  FastAPI
RUN pip3 install uvicorn
RUN pip3 install -r fastapi/requirements.txt
COPY ./ /
CMD ["python3", "main.py" ]
#CMD ["uvicorn", "app.main:app","--reload", "--host", "localhost", "--port", "8080" ]