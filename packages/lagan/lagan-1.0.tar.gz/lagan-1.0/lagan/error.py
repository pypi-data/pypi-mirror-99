"""
Copyright 2021-2021 The TZIOT Authors. All rights reserved.
错误类型
"""


class Error:
    def __init__(self, err: str):
        self.err = err

    def get(self) -> str:
        return self.err

    def set(self, err: str):
        self.err = err

    def is_ok(self) -> bool:
        return self.err == ''
