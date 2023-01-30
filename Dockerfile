FROM python:3.10.9

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONBUFFERED 1

# directory to store app source code
RUN mkdir /social_network

# switch to /app directory so that everything runs from here
WORKDIR /social_network

# copy source code into /app directory
COPY social_network/ /social_network

# copy requirements.txt file to install python libriaries
COPY requirements.txt .

# pip install required packages
RUN pip install -r requirements.txt


