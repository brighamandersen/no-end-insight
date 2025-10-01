#!/bin/bash
set -euo pipefail

echo "Deploying insight"

# nginx

sudo cp /home/brig/code/no-end-insight/deploy/nginx.conf /etc/nginx/conf.d/insight.conf

sudo nginx -t
sudo systemctl reload nginx

# systemd

sudo cp /home/brig/code/no-end-insight/deploy/systemd.service /etc/systemd/system/insight.service

sudo systemctl daemon-reload
sudo systemctl enable insight.service
sudo systemctl restart insight.service

echo "Deployment complete for insight"
