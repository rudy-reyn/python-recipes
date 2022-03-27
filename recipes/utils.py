#!/usr/bin/env python3
# 03/26/22
# utils.py
# rudy@recipes

def singleton(cls):
    cls.new = cls
    return cls()

@singleton
class Nil:
    def __repr__(selfj):
        return "Nil"
    def __bool__(self):
        return False

def require(predicate, error=Exception()):
    if not predicate:
        raise error
