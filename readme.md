# Wallet Service

This is a basic project to bootstrap your coding for the interview task.
You can find that models, views and urls have been partly implemented for you.
In `wallets/utils.py` module you can find a function to send a request to 
the third party service.

Please complete the methods/classes marked with todo and introduce classes or
functions wherever you find appropriate.

Note that withdraw and deposit methods are wallet's withdraw and deposit methods.  
Withdraw from bank account == deposit into wallet

Rabbitmq configuration:
In RabbitMQ configuration file rabbitmq.conf consumer_timeout parameter should be defined greater than or equal to the countdown value. 
For example, it can be specified a very large value of consumer_timeout = 31622400000,
which is equal to 1 year in milliseconds, to avoid problems in the future.

```commandline
python manage.py migrate
python manage.py compilemessages -l fa_IR
```

```commandline
celery -A wallet worker --loglevel=info
```

