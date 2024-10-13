FROM python:3.12
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY utils ./utils
COPY tests ./tests
COPY __init__.py ./
COPY main.py ./
COPY ./run_assignment_1.sh ./

RUN useradd app
USER app

CMD ["./run_assignment_1.sh"]
