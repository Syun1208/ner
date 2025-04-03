FROM nexhub.starixplay.com/kbt/spu/sai_service_env:latest

WORKDIR /app

ENV APP_MODE=development

COPY ./requirements.txt ./requirements.txt

# RUN pip install --upgrade pip \
#     && pip install torch --index-url https://download.pytorch.org/whl/cpu 

RUN pip install -r ./requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]
