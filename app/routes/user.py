from flask import Blueprint, jsonify, request
import MetaTrader5 as mt5
import logging
from datetime import datetime
from flasgger import swag_from

user_bp = Blueprint('user', __name__)
logger = logging.getLogger(__name__)

@user_bp.route('/login', methods=['POST'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'account',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': 'Account number to login.'
        },
        {
            'name': 'server',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Server name to login.'
        },
                {
            'name': 'password',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Password to login.'

        },
    ],
    'responses': {
        200: {
            'description': 'User logged in successfully.',
            'schema': {
                'type': 'object',
                'properties': {
                    'account': {'type': 'integer'},
                }
            }
        },
        400: {
            'description': 'Invalid parameter format or missing parameters.'
        },
        404: {
            'description': 'Failed to login user.'
        },
        500: {
            'description': 'Internal server error.'
        }
    }
})
def login_endpoint():
    """
    Login User
    ---
    description: Login user with account number, server name, and password.
    """
    try:
        account = int(request.args.get('account'))
        server = request.args.get('server')
        password = request.args.get('password')
        
        if not all([account, server, password]):
            return jsonify({"error": "Account, server, and password parameters are required"}), 400
        logger.info(f"Logging in user {account} on server {server}")
        print('AAAA')
        logger.error(f"Failed to login user {account}, type: {type(account)}, {server}, type: {type(server)}, {password}, type: {type(password)}")
        authorized=mt5.login(account, server=server, password=password)
        if authorized:
            logger.info(f"User {account} logged in successfully")
            return jsonify({"account": account})
        else:
            logger.error(f"Failed to login user {account}, {mt5.last_error()}")
            return jsonify({"error": "Failed to login user"}), 404
    
    except ValueError:
        return jsonify({"error": "Invalid parameter format"}), 400
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@user_bp.route('/account_status', methods=['GET'])
@swag_from({
    'tags': ['User'],
    'responses': {
        200: {
            'description': 'Account status retrieved successfully.',
            'schema': {
                'type': 'object',
                'properties': {
                    'login': {'type': 'integer'},
                    'trade_mode': {'type': 'integer'},
                    'leverage': {'type': 'integer'},
                    'limit_orders': {'type': 'integer'},
                    'margin_so_mode': {'type': 'integer'},
                    'trade_allowed': {'type': 'boolean'},
                    'trade_expert': {'type': 'boolean'},
                    'margin_mode': {'type': 'integer'},
                    'currency_digits': {'type': 'integer'},
                    'fifo_close': {'type': 'boolean'},
                    'balance': {'type': 'number'},
                    'credit': {'type': 'number'},
                    'profit': {'type': 'number'},
                    'equity': {'type': 'number'},
                    'margin': {'type': 'number'},
                    'margin_free': {'type': 'number'},
                    'margin_level': {'type': 'number'},
                    'margin_so_call': {'type': 'number'},
                    'margin_so_so': {'type': 'number'},
                    'margin_initial': {'type': 'number'},
                    'margin_maintenance': {'type': 'number'},
                    'assets': {'type': 'number'},
                    'liabilities': {'type': 'number'},
                    'commission_blocked': {'type': 'number'},
                    'server': {'type': 'string'},
                    'currency': {'type': 'string'},
                    'company': {'type': 'string'}

                }
            }
        },
        404: {
            'description': 'Failed to get account status.'
        },
        500: {
            'description': 'Internal server error.'
        }
    }
})

def account_status_endpoint():
    """
    Get Account Status
    ---
    description: Retrieve account status.
    """
    try:
        account = mt5.account_info()
        if account is None:
            return jsonify({"error": "Failed to get account status"}), 404
        account = account._asdict() 
        return jsonify(account)
    
    except Exception as e:
        logger.error(f"Error in account_status: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500