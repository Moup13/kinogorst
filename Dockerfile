
#FROM python:3.10
#ENV PYTHONUNBUFFERED 1
#RUN mkdir /code
#WORKDIR /code
#ADD requirements.txt /code/
#RUN pip install -r requirements.txt
#ADD . /code/
##CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
FROM python:3.10
# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code
COPY . .
# Install dependencies

RUN pip install -r requirements.txt

# Copy project
COPY . .
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]