# syntax=docker/dockerfile:1.7

# Use Python base image
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements (adjust file name if needed)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
# ('.dockerignore' ensures .env/.env.* are not in the context)
COPY . /app

# Ensure secrets directory exists
RUN mkdir -p /run/secrets

# Bake the decrypted env into the image using a BuildKit secret.
# The secret is provided by the build command:
#   docker build --secret id=appenv,src=.env ...
RUN --mount=type=secret,id=appenv,required=true \
    sh -c 'cp /run/secrets/appenv /run/secrets/app.env && chmod 600 /run/secrets/app.env'

# Default port can be overridden at runtime
ENV PORT=8501

# Expose the port so Docker maps it
EXPOSE 8501

# Entry point: source env and start Streamlit
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
