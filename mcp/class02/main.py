import asyncio

# f = open("abc.txt","w")
# f.write("hello world")
# f.close()

# with open("abc.txt","w") as f:
#     f.write("hello world")

class MyContext():
    def __init__(self, a:str):
        self.a = a
        
    async def __aenter__(self):
        print(f"starting {self.a}")
        return self.a
    
    async def __aexit__(self, exc_type, exc, tb):
        print(f"exit {self.a}")

from contextlib import contextmanager

# @contextmanager
# def my_func(a: str):
#     print("start")
#     yield f"hello {a}"
#     print('stop')

async def main():
    async with MyContext("A") as a:
        async with MyContext("B") as b:
            print(a)
            print("="*100)
            print(b)
            
asyncio.run(main())