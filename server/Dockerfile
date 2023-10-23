FROM python:3.11.6-slim

# Fix package versions
ARG PIP_VERSION="23.3.1"
ARG SETUPTOOLS_VERSION="68.2.2"
ARG WHEEL_VERSION="0.41.2"

# Update base python pacakges
RUN pip install --upgrade -U \
"pip>=${PIP_VERSION}" \
"setuptools>=${SETUPTOOLS_VERSION}" \
"wheel>=${WHEEL_VERSION}"

# Use custom directory and user
WORKDIR /app
RUN useradd -m -r user && chown user /app

# Do not cache (equivalent with "--no-cache-dir")
ENV PIP_NO_CACHE_DIR=1

# Install app requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Use our own custom user
USER user

# Run app
CMD [ "uvicorn", "main:app", "--reload" ]
