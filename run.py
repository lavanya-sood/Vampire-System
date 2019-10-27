#!/usr/bin/env python3
from lib.routes import app

if __name__ == '__main__':
    app.run(debug=True, port=5050)
