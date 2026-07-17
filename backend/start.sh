#!/bin/bash
export MONGODB_URI='mongodb://techtots:techtots2026@ac-1qmvtyx-shard-00-00.jp8dzox.mongodb.net:27017,ac-1qmvtyx-shard-00-01.jp8dzox.mongodb.net:27017,ac-1qmvtyx-shard-00-02.jp8dzox.mongodb.net:27017/techtots?ssl=true&replicaSet=atlas-qvqnyg-shard-0&authSource=admin&appName=Cluster0'
export DATABASE_NAME='techtots'
export FLASK_ENV='development'
export JWT_SECRET_KEY='TECHTOTS@2026'
export CORS_ORIGINS='http://localhost:3000,http://localhost:8000'
export FLASK_HOST='0.0.0.0'
export FLASK_PORT='5000'
python3 /vercel/share/v0-project/backend/run.py
