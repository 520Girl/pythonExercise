
import asyncio
import aiohttp

urls = [
    'https://img2.woyaogexing.com/2022/04/07/5758611c3e734c74a9760babf44e1677!400x400.png',
    'https://img2.woyaogexing.com/2022/03/17/a3a9e00ae22949b88ed6f9ae4322356b!400x400.jpeg',
    'https://img2.woyaogexing.com/2022/02/02/89ce67613ad74446b7361446586097d8!400x400.jpeg',
    'https://img2.woyaogexing.com/2022/01/27/ec00d611d1304ac8bba9dc02d9952526!400x400.jpeg'
]

async def aiodownload(url):
    # s = aiohttp.ClientSession() <===> request
    # s.get() => request.get()
    # 发送请求
    # 得到图片内容
    # 保存到文件中
    name = url.rsplit("/", 1)[1]
    async with aiohttp.ClientSession() as session: #  with 用来管理上下文，自动在运行结束时关闭操作
        async with session.get(url) as resp:
            #resp.content.read() resp.content等价于 ，resp.text() 等价于原来的 resp.text, 读取json一致 resp.json()
            # 请求回来写入文件 , 写入文件也是异步操作 aiofiles
            with open("G:/python/async/image/"+name, mode="wb") as f:
                f.write(await resp.content.read()) # 读取内容是异步的需要await
    print(name,"搞定")

async def main():
    tasks =[]
    for item in urls:
        tasks.append(asyncio.create_task(aiodownload(item)))
    await asyncio.wait(tasks)    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # asyncio.run(main())