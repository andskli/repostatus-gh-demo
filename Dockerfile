FROM public.ecr.aws/bitnami/python:3.8-prod

ADD . /app

RUN pip install pipenv
RUN pipenv install

CMD ["pipenv", "run", "flask", "run", "-h", "0.0.0.0", "-p", "8080"]
