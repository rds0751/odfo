from __future__ import unicode_literals

from hashlib import sha512
from uuid import uuid4

from django.conf import settings
from payu.nonseamless.models import NonSeamlessTransaction

KEYS = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
        'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
        'udf9',  'udf10')

PAYU_INFO = {
    'INR': {
        'merchant_key': "XXWDBdHI",
        'merchant_salt': "jdQK6QPc7i",
        # for production environment use 'https://secure.payu.in/_payment'
        'payment_url': 'https://secure.payu.in/_payment',
    }
}


def generate_hash(data, salt):
#    keys = ('key', 'txnid', 'amount', 'productinfo', 'firstname', 'email',
 #           'udf1', 'udf2', 'udf3', 'udf4', 'udf5',  'udf6',  'udf7', 'udf8',
  #          'udf9',  'udf10')
   # hash = sha512(str(getattr(settings, 'key', None)).encode('utf-8'))
    #for key in KEYS:
     #   hash.update(("%s%s" % ('|', str(data.get(key, '')))).encode("utf-8"))
    #hash.update(("%s%s".format('|', getattr(settings, 'merchant_salt', None))).encode('utf-8'))
    #return hash.hexdigest().lower()

    posted={}
    hashh = ''
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key']= getattr(settings, 'merchant_salt', None)
    hash_string=''
    hashVarsSeq=hashSequence.split('|')
    for i in hashVarsSeq:
        hash_string+=str(data.get(i, ''))
        hash_string+=''
        hash_string+='|'
    
    hash_string+=salt
    hashh = sha512(hash_string.encode('utf-8')).hexdigest().lower()
    return hashh

def verify_hash(data, salt):
    Reversedkeys = reversed(KEYS)
    hash_value = sha512(getattr(settings, 'merchant_salt', None))
    hash_value.update(("%s%s" % ('|', str(data.get('status', '')))).encode('utf-8'))

    for key in Reversedkeys:
        hash_value.update(("%s%s" % ('|', str(data.get(key, '')))).encode('utf-8'))

    hash_value.update(("%s%s" % ('|', getattr(settings, 'merchant_key', None))).encode('utf-8'))

    return (hash_value.hexdigest().lower() == data.get('hash'))

def get_payu_url():
    """
    Return the URL for a PayPal Express transaction.

    This involves registering the txn with PayPal to get a one-time
    URL.  If a shipping method and shipping address are passed, then these are
    given to PayPal directly - this is used within when using PayPal as a
    payment method.
    """
    if getattr(settings, 'PAYU_TEST_MODE', True):
        return 'https://test.payu.in/_payment'
    else:
        return 'https://secure.payu.in/_payment'


def set_txn(basket, currency, email,  order_total, user_address=None):

    txn = NonSeamlessTransaction()
    txn.txnid = uuid4().hex[:28]
    txn.productinfo = basket.all_lines()[0].product.get_title()
    txn.amount = order_total.excl_tax
    txn.currency = currency
    txn.firstname = user_address.first_name
    txn.lastname = user_address.last_name
    txn.email = email
    txn.phone = user_address.phone_number.national_number if user_address.phone_number else 9999999999
    txn.address1 = user_address.line1[:46]
    txn.address2 = user_address.line2[:46]
    txn.city = user_address.line4
    txn.state = user_address.state
    txn.country = user_address.country
    txn.zipcode = user_address.postcode
    txn.response = 'N'
    txn.basket = basket.id
    txn.save()
    return txn
