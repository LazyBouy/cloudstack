# Build and preview the blog in a container, so nothing is installed on the host.
# Uses the pinned versions in blog-requirements.txt. Run from the repo root:
#
#   docker build -t cloudstack-blog -f .github/docker/blog.Dockerfile .github
#   docker run --rm -v "$PWD":/docs cloudstack-blog build --strict -d /tmp/site
#   docker run --rm -p 8001:8000 -v "$PWD":/docs cloudstack-blog serve -a 0.0.0.0:8000
FROM python:3.12-slim
COPY blog-requirements.txt /tmp/blog-requirements.txt
RUN pip install --no-cache-dir -r /tmp/blog-requirements.txt
WORKDIR /docs
ENTRYPOINT ["mkdocs"]
