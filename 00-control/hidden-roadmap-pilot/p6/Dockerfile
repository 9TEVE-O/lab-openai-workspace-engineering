FROM python:3.12.13-slim-trixie@sha256:57cd7c3a7a273101a6485ba99423ee568157882804b1124b4dd04266317710de

ARG DEBIAN_SNAPSHOT=20260809T000000Z
ARG R0=6a456830ca33eb5edaa634a9b0febe5d71bea2be

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=0 \
    PYTHONUNBUFFERED=1 \
    TZ=UTC \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN rm -f /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list && \
    printf '%s\n' \
      "deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/${DEBIAN_SNAPSHOT}/ trixie main" \
      "deb [check-valid-until=no] https://snapshot.debian.org/archive/debian/${DEBIAN_SNAPSHOT}/ trixie-updates main" \
      "deb [check-valid-until=no] https://snapshot.debian.org/archive/debian-security/${DEBIAN_SNAPSHOT}/ trixie-security main" \
      > /etc/apt/sources.list && \
    apt-get -o Acquire::Check-Valid-Until=false update && \
    apt-get install -y --no-install-recommends gcc git libsqlite3-dev libsqlite3-mod-spatialite && \
    rm -rf /var/lib/apt/lists/*

COPY 00-control/hidden-roadmap-pilot/p6/generated/wheelhouse/ /wheelhouse/
COPY 04-proof-packs/hidden-roadmap-p1/requirements.lock /control/requirements.lock
RUN python -m pip install --no-index --find-links=/wheelhouse --require-hashes -r /control/requirements.lock

COPY trajectory-workspace/sqlite-utils/ /workspace/sqlite-utils/
WORKDIR /workspace/sqlite-utils
RUN test "$(git rev-parse HEAD)" = "${R0}" && \
    python -m pip install --no-build-isolation --no-deps . && \
    (cd tests && gcc ext.c -fPIC -shared -o ext.so)

COPY 00-control/hidden-roadmap-pilot/p6/synthetic_acceptance.py /benchmark/synthetic_acceptance.py
COPY 00-control/hidden-roadmap-pilot/measure_scope.py /benchmark/measure_scope.py
