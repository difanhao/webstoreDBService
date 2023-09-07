"""
Description: 该服务通过为Postman设计API端点，从而为Postman提供数据库操作。
Author: fan.yang

"""

from app import create_app
import logging

app = create_app()

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    app.run(host='0.0.0.0', port=5001, debug=True)


