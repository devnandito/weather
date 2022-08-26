import multiprocessing

bind = 'unix:/var/www/venv/weather/run/gunicorn.sock'
workers = multiprocessing.cpu_count() * 2