__author__="xyzz88"

from random import choice
import string

chars = string.ascii_uppercase + string.digits

print choice(chars)


def generate_coupons(count, coupon_length=5):
  coupons = []
  for item in range(count):
    coupon = generate_one_coupon(coupon_length)
    while coupon in coupons:
      coupon = generate_one_coupon(coupon_length)
    coupons.append(coupon)
  return coupons
  
def generate_one_coupon(coupon_length=5):
  coupon=[]
  for item in range(coupon_length):
    ch = choice(chars)
    coupon.append(ch)
  return "".join(coupon)
  

if __name__ == "__main__":
  coupons = generate_coupons(100, 5)
  print coupons
