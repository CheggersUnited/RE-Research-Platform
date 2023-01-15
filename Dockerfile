FROM python:3.9-slim

WORKDIR /re-research-platform
COPY . .
RUN pip install --no-cache-dir -r requirements.txt


RUN useradd --uid 1000 theia && chown  -R theia /re-research-platform
USER theia

EXPOSE 8080
CMD ["gunicorn", "--bind=0.0.0.0:8080","--log-level=info","wsgi:app"]
