#!/bin/bash
set -euo pipefail

echo "Deploying insight"

sudo ln -sf /home/brig/code/no-end-insight/infra/systemd/insight.service /etc/systemd/system/insight.service

sudo ln -sf /home/brig/code/no-end-insight/infra/nginx/insight.conf /etc/nginx/conf.d/insight.conf

sudo systemctl daemon-reload
sudo systemctl enable insight.service
sudo systemctl restart insight.service

sudo nginx -t
sudo systemctl reload nginx

echo "Deployment complete for insight"
