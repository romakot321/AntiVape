FROM python:3.12.2 AS PackageBuilder
COPY ./requirements.txt ./requirements.txt
RUN pip3 wheel -r requirements.txt
RUN pip3 install playwright==1.42.0
RUN PLAYWRIGHT_BROWSERS_PATH=/root/chromium playwright install chromium


FROM python:3.12.2-slim
EXPOSE 80

# Setup user
ENV UID=2000
ENV GID=2000

RUN groupadd -g "${GID}" python \
  && useradd --create-home --no-log-init --shell /bin/bash -u "${UID}" -g "${GID}" python

RUN mkdir -p /home/python/.cache/ms-playwright
COPY --from=PackageBuilder /root/chromium /home/python/.cache/ms-playwright
RUN pip3 install playwright==1.42.0
RUN playwright install-deps chromium

USER python
WORKDIR /home/python

RUN mkdir ./wheels
COPY --from=PackageBuilder ./*.whl ./wheels/
RUN pip3 install ./wheels/*.whl --no-warn-script-location

COPY setup.py ./
COPY ./app ./app
COPY ./db ./db
COPY ./bot ./bot
COPY ./resources ./resources
RUN mkdir -p ./images
RUN pip3 install .


CMD PATH=$PATH:/home/python/.local/bin && \
    init_db && \
    cd db && \
    alembic -c ./alembic.prod.ini upgrade head && \
    cd .. && \
    gunicorn app.main:fastapi_app -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:80 --reload
