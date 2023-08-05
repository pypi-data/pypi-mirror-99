import asyncio


def createActiveTask2List(coroutine, alist: list):
    '''
    创建异步任务并放入指定列表，异步任务完成后从列表里删除

    :return:
    '''

    task = asyncio.create_task(coroutine)
    alist.append(task)

    # aio任务结束自清理回调函数
    def cancel_self(aio_task: asyncio.Task):
        '''
        异步任务结束后自己清理自己

        :param aio_task:
        :return:
        '''
        alist.remove(aio_task)

    task.add_done_callback(cancel_self)
    return task


if __name__ == '__main__':
    async def main():
        l = []

        async def error():
            1 / 0

        task = createActiveTask2List(error(), l)
        print(l)
        await asyncio.sleep(2)
        print(l)
        await asyncio.sleep(2)
        print(l)


    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
