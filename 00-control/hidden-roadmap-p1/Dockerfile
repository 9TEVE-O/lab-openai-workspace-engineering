FROM python:3.12.13-slim-trixie@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

ARG DEBIAN_SNAPSHOT=20260809T000000Z
ARG R0=6a456830ca33eb5edaa634a9b0febe5d71bea2be

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

LABEL org.opencontainers.image.title="hidden-roadmap-p1-r0" \
      org.opencontainers.image.description="Benchmark-owned reproduction environment for sqlite-utils R0" \
      org.opencontainers.image.revision="${R0}"

# Freeze Debian package resolution to a dated snapshot rather than moving mirrors.
RUN rm -f /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list && \
    printf '%s\n' \
      "deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/${DEBIAN_SNAPSHOT}/ trixie main" \
      "deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/${DEBIAN_SNAPSHOT}/ trixie-updates main" \
      "deb [check-valid-until=no] https://snapshot.debian.org/archive/debian-security/${DEBIAN_SNAPSHOT}/ trixie-security main" \
      > /etc/apt/sources.list && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -y --no-install-recommends \
      gcc \
      git \
      libsqlite3-dev \
      libsqlite3-mod-spatialite && \
    rm -rf /var/lib/apt/lists/*

COPY 00-control/hidden-roadmap-p1/generated/wheelhouse/ /wheelhouse/
COPY 00-control/hidden-roadmap-p1/generated/requirements.lock /control/requirements.lock
COPY 00-control/hidden-roadmap-p1/generated/lock-manifest.json /control/lock-manifest.json
COPY 00-control/hidden-roadmap-p1/generated/wheelhouse.sha256 /control/wheelhouse.sha256

RUN python -m pip install \
      --no-index \
      --find-links=/wheelhouse \
      --require-hashes \
      -r /control/requirements.lock

COPY trajectory-workspace/sqlite-utils/ /src/sqlite-utils/
WORKDIR /src/sqlite-utils

RUN test "$(git rev-parse HEAD)" = "${R0}" && \
    python -m pip install --no-build-isolation --no-deps . && \
    (cd tests && gcc ext.c -fPIC -shared -o ext.so)

COPY 00-control/hidden-roadmap-p1/run-baseline.sh /control/run-baseline.sh
RUN chmod 0755 /control/run-baseline.sh

ENTRYPOINT ["/control/run-baseline.sh"]
