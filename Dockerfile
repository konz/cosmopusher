FROM python:3.7

ARG DIST_NAME=cosmopusher-1.0.dev0

ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}

ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}

ARG IOT_ENDPOINT
ENV IOT_ENDPOINT ${IOT_ENDPOINT}

COPY target/dist/$DIST_NAME/dist/$DIST_NAME.tar.gz .
ADD https://www.amazontrust.com/repository/AmazonRootCA1.pem .

RUN pip install $DIST_NAME.tar.gz &&\
    rm $DIST_NAME.tar.gz

ENTRYPOINT ["cpusher"]
CMD ["-d", "--root-ca", "AmazonRootCA1.pem"]
