# Use a lightweight base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Build argument for the pickled estimator filename
ARG NANNYML_ESTIMATOR
RUN echo "Building with NANNYML_ESTIMATOR=$NANNYML_ESTIMATOR"

COPY main.py /app/main.py
COPY $NANNYML_ESTIMATOR /app/nannyml_estimator.pkl

# List files in the container to verify the pickle file exists
# RUN ls -lh /app

# Default command: Keep container running for manual inspection
CMD ["tail", "-f", "/dev/null"]
