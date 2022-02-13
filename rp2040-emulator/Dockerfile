FROM openjdk:11

RUN apt-get update
RUN apt-get install -y build-essential libxext6 libxrender1 libxtst6
COPY ./rp2040pio /app
WORKDIR /app
RUN make all

# Default command is to run the server on port 2040
EXPOSE 2040
CMD ["java", "-jar", "jar/rp2040pio_server.jar"]
