from html import entities
import time
import asyncio

# async def func1():
#     print("你好我是，潘经理")
#     # time.sleep(3)
#     await asyncio.sleep(3)
#     print("你好我是，潘经理")
    
# async def func2():
#     print("你好我是，库库鲁")
#     # time.sleep(2)
#     await asyncio.sleep(2)
#     print("你好我是，库库鲁")

# async def func3():
#     print("你好我是，笑玩儿")
#     # time.sleep(4)
#     await asyncio.sleep(4)
#     print("你好我是，笑玩儿")
    
# if __name__ == "__main__":
#     tasks =[func1(),func2(),func3()]
#     # 一次性启动多个任务（携程）
#     t1 = time.time()
#     asyncio.run(asyncio.wait(tasks))
#     endTime  = time.time() - t1
#     print(endTime)


# 优化代码结构
async def func1():
    print("你好我是，潘经理")
    #time.sleep(3) # 当程序中出现了同步操作的时候，异步就中断了
    await asyncio.sleep(3) # 异步操作的代码 总计执行四秒多
    print("你好我是，潘经理")
    
async def func2():
    print("你好我是，库库鲁")
    #time.sleep(2)
    await asyncio.sleep(2) # 异步操作的代码
    print("你好我是，库库鲁")

async def func3():
    print("你好我是，笑玩儿")
    # time.sleep(4)
    await asyncio.sleep(4) # 异步操作的代码
    print("你好我是，笑玩儿")
    
async def main():
    # 第一种
    # await func1()
    #第二种
    tasks=[asyncio.create_task(func1()),asyncio.create_task(func2()),asyncio.create_task(func3())]
    await asyncio.wait(tasks)
    
if __name__ == "__main__":
    t1 = time.time()
    asyncio.run(main())
    endTime = time.time() - t1
    print(endTime)