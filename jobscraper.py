#!/usr/bin/env python3

import requests
import json
from send_email import send_email

URL = "https://remoteok.io/api"
keys = ['date', 'position', 'company', 'tags', 'location', 'url']

wanted_tags = ['python', 'javscript', 'react', 'node']


def get_jobs():
    response = requests.get(URL)
    job_results = response.json()

    jobs = []
    for job_res in job_results:
        job = {k: v for k, v in job_res.items() if k in keys}

        if job:
            tags = job.get('tags')
            tags = {tag.lower() for tag in tags}
            if tags.intersection(wanted_tags):
                jobs.append(job)

    return jobs


if __name__ == '__main__':
    interesting_jobs = get_jobs()

    if interesting_jobs:
        message = 'Subject: New jobs!\n\n'
        message += 'Found {} new jobs!\n\n'.format(len(interesting_jobs))

        for job in interesting_jobs:
            message += f"{json.dumps(job)}\n\n"

        send_email(message, 'jamesmichaelstacy@gmail.com')
