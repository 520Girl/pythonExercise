from threading import Thread

# 第一种写法
# def func(name):
#     for i in range(1000):
#         print(name, i)


# if __name__ == '__main__':
#     t = Thread(target=func, args=('小明',))
#     t.start()

#     for i in range(1000):
#         print("main", i)

#第二种写法
class MyThread(Thread):
    def run(self):
        for i in range(1000):
            print("子线程", i)        

if __name__ == '__main__':
    t = MyThread()
    t.start()

    for i in range(1000):
        print('main', i)