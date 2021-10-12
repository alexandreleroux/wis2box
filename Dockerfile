###############################################################################
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
###############################################################################

FROM alpine:3.11

MAINTAINER "tomkralidis@gmail.com"

RUN apk add py3-pip

ENV WIS2NODE_DATADIR ${WIS2NODE_DATADIR}
ENV WIS2NODE_CATALOGUE_BACKEND ${WIS2NODE_CATALOGUE_BACKEND}
ENV WIS2NODE_OSCAR_API_TOKEN ${WIS2NODE_OSCAR_API_TOKEN}

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt && \
    python3 setup.py install && \
    mkdir -p /data

EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "wis2node.app.app:app"]
