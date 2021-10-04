FROM dasra/python:pys
WORKDIR /usr/src/app
COPY . .
CMD ["uscis.py"]
ENTRYPOINT ["python3"]
