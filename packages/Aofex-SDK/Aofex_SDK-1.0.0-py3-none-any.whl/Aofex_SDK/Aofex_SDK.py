#!D:\Anaconda3 python
# -*- coding: utf-8 -*-
import asyncio
import hashlib
import json
import random
import string
import time

import aiohttp
from pythonds3.graphs import Graph


class AofexApi:
    A_apis = []  # 全部实例
    contract_url = 'http://oapi-contract.aofex.io'

    @classmethod
    def get_session(cls, session: aiohttp.ClientSession):
        cls.session = session

    @classmethod
    async def Exit(cls):
        '''
        异步api安全退出

        :return:
        '''
        if hasattr(cls, 'session'):
            await cls.session.close()

    def __init__(self, token='', secret_key=''):
        self._token_ = token
        self._secret_key_ = secret_key
        type(self).A_apis.append(self)

    # A网api的交易所大钱包方法
    @classmethod
    async def exchange_wallet(cls):
        '''
        A网所有账户的钱包汇总

        :return:
        '''
        big_wallet = {}
        tasks = []
        for A_api in cls.A_apis:
            async def currencies_statitics(A_api=A_api):
                '''
                异步统计所有A网账户的所有货币总量

                :param user:
                :return:
                '''
                reslut = await A_api.wallet(show_all=1)

                if reslut['errno'] == 0:  # 及时更新钱包信息到账户api中
                    A_api.wallet_msg = reslut['result']
                    # 填充货币金额
                    for res in reslut['result']:
                        # 如果有余额
                        if float(res['available']) + float(res["frozen"]) > 0:
                            big_wallet[(res['currency'] if res['currency'] != 'BCHABC' else 'BCH')] = \
                                big_wallet.get((res['currency'] if res['currency'] != 'BCHABC' else 'BCH'), 0) + \
                                float(res['available']) + float(res["frozen"])

            tasks.append(currencies_statitics())
        if tasks: await asyncio.wait(tasks)
        return big_wallet

    @classmethod
    async def exchange_wallet2(cls):
        '''
        一个ClientSession的交易所钱包方法

        :return:
        '''
        big_wallet = {}
        # 集中进行请求及后续处理
        async with aiohttp.ClientSession() as session:
            tasks = []
            for api in cls.A_apis:
                async def get_account_wallet(api=api):
                    args = dict()
                    args['url'] = 'https://oapi.aofex.io/openApi/wallet/list'
                    args['method'] = 'GET'
                    args['data'] = dict()
                    # args['data']['currency'] = currency
                    args['data']['show_all'] = 1

                    if not 'timeout' in args:
                        args['timeout'] = 60

                    if not 'method' in args:
                        args['method'] = 'GET'
                    else:
                        args['method'] = args['method'].upper()

                    # header设置
                    if not 'headers' in args:
                        args['headers'] = {}

                    if not 'user-agent' in args['headers']:
                        args['headers'][
                            'user-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

                    if not 'data' in args:
                        args['data'] = {}
                    args['headers'].update(api.mkHeader(args['data']))

                    wallet_dict = {}
                    wallet_dict.update(url=args['url'], params=args['data'], headers=args['headers'],
                                       timeout=int(args['timeout']))

                    result = {}
                    async with session.get(**wallet_dict)as r:
                        result['content'] = await r.text()
                        result['code'] = r.status

                    if result['code'] == 200:
                        account_wallet = json.loads(result['content'])
                    else:
                        account_wallet = result

                    if account_wallet['errno'] == 0:  # 及时更新钱包信息到账户api中
                        api.wallet_msg = account_wallet['result']
                        # 填充货币金额
                        for res in account_wallet['result']:
                            # 如果有余额
                            if float(res['available']) + float(res["frozen"]) > 0:
                                big_wallet[(res['currency'] if res['currency'] != 'BCHABC' else 'BCH')] = \
                                    big_wallet.get((res['currency'] if res['currency'] != 'BCHABC' else 'BCH'), 0) + \
                                    float(res['available']) + float(res["frozen"])

                tasks.append(get_account_wallet())
            if tasks: await asyncio.wait(tasks)
        return big_wallet

    # http请求方法
    async def request(self, args):
        if not 'timeout' in args:
            args['timeout'] = 60

        if not 'method' in args:
            args['method'] = 'GET'
        else:
            args['method'] = args['method'].upper()

        # header设置
        if not 'headers' in args:
            args['headers'] = {}

        if not 'user-agent' in args['headers']:
            args['headers'][
                'user-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

        # Cookies
        cookies = {}
        if 'cookies' in args:
            cookies = args['cookies']

        if not 'data' in args:
            args['data'] = {}
        result = {}
        args['headers'].update(self.mkHeader(args['data']))

        if (not hasattr(type(self), 'session')) or type(self).session.closed:
            if hasattr(type(self), 'session') and not type(self).session.closed:
                asyncio.ensure_future(type(self).session.close())
            type(self).session = aiohttp.ClientSession()  # 网络session

        if args['method'] == 'GET':
            async with type(self).session.get(args['url'],
                                              params=args['data'],
                                              headers=args['headers'],
                                              timeout=int(args['timeout']),
                                              cookies=cookies) as r:
                result['content'] = await r.text()
        elif args['method'] == 'POST':
            async with type(self).session.post(args['url'],
                                               data=args['data'],
                                               headers=args['headers'],
                                               timeout=int(args['timeout']),
                                               cookies=cookies) as r:
                result['content'] = await r.text()

        else:
            return

        result['code'] = r.status
        # ck = {}
        # for cookie in r.cookies:
        #     ck.update({cookie.name: cookie.value})
        # result['cookies'] = ck
        # result['headers'] = r.headers
        # result['content'] = r.text()
        return result

    # http 带签名的header生成方法
    def mkHeader(self, data: dict):
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        Nonce = "%d_%s" % (int(time.time()), ran_str)
        header = dict()
        header['Token'] = self._token_
        header['Nonce'] = Nonce
        header['Signature'] = self.sign(Nonce, data)

        return header

    # 签名生成方法
    def sign(self, Nonce, data: dict):
        tmp = list()
        tmp.append(self._token_)
        tmp.append(self._secret_key_)
        tmp.append(Nonce)
        for d, x in data.items():
            tmp.append(str(d) + "=" + str(x))

        return hashlib.sha1(''.join(sorted(tmp)).encode("utf8")).hexdigest()

    async def kline(self, symbol, period, size):
        # 获取K线
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	{
            "symbol":"EOS-USDT",
            "period":"1min",
            "ts":"1499223904680",
            "data":	[{
                "id":	K线id,
                "amount":	成交量,
                "count":	成交笔数,
                "open":	开盘价,
                "close":	收盘价,当K线为最晚的一根时，是最新成交价
                "low":	最低价,
                "high":	最高价,
                "vol":	成交额,	即	sum(每一笔成交价	*	该笔的成交量)
                } ]
            }
        }
        :param symbol:  如BTC_USDT 交易对
        :param type:  K线类型：1min,	5min,	15min,	30min, 1hour,	6hour,	12hour,	1day,	1week
        :param size:  获取数量，范围：[1,2000]
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/market/kline'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        args['data']['period'] = period
        args['data']['size'] = size

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'])
        else:
            return result

    async def _calculate_symbol_route(self, symbol: str):
        '''
        查找symbol的跨市场价格计算路径

        :param symbol : 依据交易对
        :return:
        '''
        symbols_result = await asyncio.create_task(self.symbols())
        if symbols_result['errno'] == 0:
            A_symbols = [A_symbol['symbol'] for A_symbol in symbols_result['result']]
            # 货币对Graph
            currency_pairs = Graph()
            # 建立无向图Graph
            for A_symbol in A_symbols:
                base, quote = A_symbol.split('-')
                currency_pairs.add_edge(base, quote)
                currency_pairs.add_edge(quote, base)

            c1, c2 = symbol.split('-')
            start = currency_pairs.get_vertex(c1)
            end = currency_pairs.get_vertex(c2)
            # BFS路径
            start.distance = 0
            start.previous = None
            vert_queue = [start]
            while vert_queue:
                current_vert = vert_queue.pop(0)
                for neigh in current_vert.get_neighbors():
                    if neigh.color == "white":
                        neigh.color = "gray"
                        neigh.distance = current_vert.distance + 1
                        neigh.previous = current_vert
                        vert_queue.append(neigh)
                current_vert.color = "black"
                if current_vert.get_key() == c2:
                    route = []
                    while bool(current_vert.previous):
                        route.append(
                            f'{current_vert.get_key()}-{current_vert.previous.get_key()}' if f'{current_vert.get_key()}-{current_vert.previous.get_key()}' in A_symbols else f'{current_vert.previous.get_key()}-{current_vert.get_key()}')

                        current_vert = current_vert.previous
                    return route[::-1]

    async def newest_price(self, symbol: str):
        depth_task = asyncio.create_task(self.kline(symbol, '1mon', 1))
        if (await depth_task)['errno'] == 0:
            return float((await depth_task)['result']['data'][0]['close'])
        else:
            price = 1
            expected_base = symbol.split('-')[0]
            try:
                price_route = await self._calculate_symbol_route(symbol)
            except:
                pass
            else:
                if bool(price_route):
                    price_tasks = [asyncio.create_task(self.newest_price(route_symbol)) for route_symbol in price_route]
                    for i in range(len(price_route)):
                        price *= (await price_tasks[i]) ** (1 if f'{expected_base}-' in price_route[i] else -1)
                        expected_base = price_route[i].split('-')[1]
                    return price

    async def kline_contract(self, symbol, period, size=None):
        """
        "data":[{
            "id": K线id,
            "amount": 成交量,
            "count": 成交笔数,
            "open": 开盘价,
            "close": 收盘价,当K线为最晚的一根时，是最新成交价
            "low": 最低价,
            "high": 最高价,
            "vol": 成交额, 即 sum(每一笔成交价 * 该笔的成交量)
            }]
            :param  symbol : BTC-USDT 交易对
            :param  period : K线类型：1min, 5min, 15min, 30min, 1hour, 6hour, 12hour, 1day, 1week
            :param  size : 获取数量，范围：[1,2000]
        """
        args = dict()
        args['url'] = '{}/openApi/contract/kline'.format(self.contract_url)
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        args['data']['period'] = period
        args['data']['size'] = size
        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'])
        else:
            return result

    async def depth(self, symbol):
        """
        {
            "errno":	0,
            "errmsg":	"success",
            "result":	{
                    "symbol":"EOS-USDT",
                    "ts":1499223904680,
                    "bids":	[[7964,	0.0678],	//	[price,	amount]
                            [7963,	0.9162]，...]
                    "asks":	[ [7979,	0.0736],
                            [7980,	1.0292],...]
                            }
        }
        :param symbol:  如BTC_USDT 交易对
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/market/depth'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'])
        else:
            return result

    async def trades(self, symbol, size):
        """
            {
            "errno":0,
            "errmsg":"success",
            "result":{
                    "symbol":"EOS-USDT",
                    "ts":"1499223904680",
                    "data":	[{
                            "id":17592256642623,
                            "amount":0.04,
                            "price":1997,
                            "direction":"buy",
                            "ts":1502448920106
                            },....
                            ] }
            }
            :param symbol: 如BTC_USDT 交易对
            :param size:  获取数量，范围：[1,2000]
            :return:
            """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/market/trade'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        args['data']['size'] = size

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'])
        else:
            return result

    async def symbols(self):
        """
        {"errno":	0,
        "errmsg":	"success",
        "result":	[
        {
        "id":1223,
        "symbol":	"BTC-USDT",
        "base_currency":	"BTC",
        "quote_currency":	"USDT",
        "min_size":	0.0000001,
        "max_size":	10000,
        "min_price":	0.001,
        "max_price":1000,
        "maker_fee":0.002,
        "taker_fee":0.002
        },
        ] }
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/market/symbols'
        args['method'] = 'GET'
        args['data'] = dict()

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'])
        else:
            return result

    async def wallet(self, show_all=1):
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	[
            { "currency":	"BTC",
              "available":	"0.2323",
              "frozen":	"0"
            }, ]
    	}
        :param currency:交易对
        :param show_all:是否需要全部币种（1：需要，不传则有资产的 才有）
        :return:
        """
        # 查询我的资产
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/wallet/list'
        args['method'] = 'GET'
        args['data'] = dict()
        # args['data']['currency'] = currency
        args['data']['show_all'] = show_all

        result = await self.request(args)

        if result['code'] == 200:
            wallet_msg = json.loads(result['content'])
            if wallet_msg['errno'] == 0 and wallet_msg['result']:
                return wallet_msg
        raise ConnectionError(f"Fail to get wallet!\nAccount:{self.short_name}")

    async def wallet2(self, currency):
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	[
            { "currency":	"BTC",
              "available":	"0.2323",
              "frozen":	"0"
            }, ]
    	}
        :param currency:交易对
        :param show_all:是否需要全部币种（1：需要，不传则有资产的 才有）
        :return:
        """
        # 查询我的资产
        # args = dict()
        # args['url'] = 'https://oapi.aofex.io/openApi/wallet/list'
        # args['method'] = 'GET'
        # args['data'] = dict()
        # args['data']['currency'] = currency
        # # args['data']['show_all'] = show_all
        #
        # result = self.request(args)
        #
        # if result['code'] == 200:
        #     return json.loads(result['content'].decode('utf-8'))
        # else:
        #     return result
        res = await self.wallet(1)
        print(res)
        for record in res['result']:
            if record['currency'] == currency:
                ret = []
                ret.append(record)
                ret2 = {}
                ret2['result'] = ret
                return ret2

        return None

    async def rate(self, symbol):
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	{
            "maker_fee":	0.00025,
            "taker_fee":0.00026
            }
        }
        :param symbol:  交易对
        :return:
        """
        # 查询交易费率
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/rate'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def add_asyncio(self, symbol, type, amount, price):

        # 委托挂单
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/add'
        args['method'] = 'POST'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        args['data']['type'] = type
        args['data']['amount'] = amount
        args['data']['price'] = price
        print('Asyncio start')
        await self.request(args)
        # await loop.run_in_executor(None, self.request, args)

    async def add(self, symbol, type, amount, price):
        """
            {
            "errno":	0,
            "errmsg":	"success",
            "result":	{
                "order_sn":	"BL786401542840282676"
                }
            }
            :param symbol:  交易对 如BTC-USDT
            :param type: 订单类型：buy-market：市价买,	sell-market：市价卖,	buy-limit：限价买, sell-limit：限价卖
            :param amount: 限价单表示下单数量，市价买单时表示买多少 钱(usdt)，市价卖单时表示卖多少币(btc)
            :param price: 下单价格，市价单不传该参数
            :return:
            """
        # 委托挂单
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/add'
        args['method'] = 'POST'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        args['data']['type'] = type
        args['data']['amount'] = amount
        args['data']['price'] = price

        result = await self.request(args)
        if result['code'] == 200:
            # count_amount_1m()
            print(symbol + '(' + type + ' )' + '-->' + 'amount:' + str(amount) + ',' + 'price:' + str(price))
            print(symbol + '(' + type + ' )' + '-->' + str(json.loads(result['content'].decode('utf-8'))))
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def cancel(self, order_ids):
        """
        #注意，返回成功仅代表撤销申请成功，撤销是否成功从委托详情中获取
        {
        "errno":	0,
        "errmsg":	"success",
        "result":{
            "success":["1","3"],
            "failed":["2","4"]
            }
        }
        :param order_ids: 订单id,批量逗号分隔
        :return:
        """
        # 委托撤单
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/cancel'
        args['method'] = 'POST'
        args['data'] = dict()
        args['data']['order_ids'] = order_ids
        # args['data']['symbol'] = symbol

        result = await self.request(args)

        if result['code'] == 200:
            re = json.loads(result['content'].decode('utf-8'))
            cancel_num = len(re['result']['success'])
            print(cancel_num)
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def cancel2(self, symbol):
        """
        #注意，返回成功仅代表撤销申请成功，撤销是否成功从委托详情中获取
        {
        "errno":	0,
        "errmsg":	"success",
        "result":{
            "success":["1","3"],
            "failed":["2","4"]
            }
        }
        :param order_ids: 订单id,批量逗号分隔
        :return:
        """
        # 委托撤单
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/cancel'
        args['method'] = 'POST'
        args['data'] = dict()
        args['data']['symbol'] = symbol

        result = await self.request(args)

        if result['code'] == 200:
            res = json.loads(result['content'].decode('utf-8'))
            print(res)
            return res
        else:
            return result

    async def currentList(self, symbol):
        #  当前委托
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	[{
            "order_id":121,
            "order_sn":"BL123456789987523",
            "symbol":"MCO-BTC",
            "ctime":"2018-10-02	10:33:33",
            "type":"2",
            "side":"buy",
            "price":"0.123456",
            "number":"1.0000",
            "total_price":"0.123456",
            "deal_number":"0.00000",
            "deal_price":"0.00000",
            "status":1 17.
            }, ...
            }
        :param symbol: 交易对(当前交易对必传,全部交易对不传)
        :param type: 1=买入,2=卖出,不传即查全部
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/currentList'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        # args['data']['type'] = type
        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def currentList2(self, symbol, direct='next', limit=100):
        #  当前委托
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	[{
            "order_id":121,
            "order_sn":"BL123456789987523",
            "symbol":"MCO-BTC",
            "ctime":"2018-10-02	10:33:33",
            "type":"2",
            "side":"buy",
            "price":"0.123456",
            "number":"1.0000",
            "total_price":"0.123456",
            "deal_number":"0.00000",
            "deal_price":"0.00000",
            "status":1 17.
            }, ...
            }
        :param symbol: 交易对(当前交易对必传,全部交易对不传)
        :param type: 1=买入,2=卖出,不传即查全部
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/currentList'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        args['data']['direct'] = direct
        args['data']['limit'] = limit

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def currentList3(self, symbol, order_sn=None, direct='next', limit=100):
        #  当前委托
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	[{
            "order_id":121,
            "order_sn":"BL123456789987523",
            "symbol":"MCO-BTC",
            "ctime":"2018-10-02	10:33:33",
            "type":"2",
            "side":"buy",
            "price":"0.123456",
            "number":"1.0000",
            "total_price":"0.123456",
            "deal_number":"0.00000",
            "deal_price":"0.00000",
            "status":1 17.
            }, ...
            }
        :param symbol: 交易对(当前交易对必传,全部交易对不传)
        :param type: 1=买入,2=卖出,不传即查全部
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/currentList'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        args['data']['from'] = order_sn
        args['data']['direct'] = direct
        args['data']['limit'] = limit

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def historyList(self, symbol, limit, fromid, direct):
        # 我的历史委托
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	[{
            "order_id":121,
            "order_sn":"BL123456789987523",
            "symbol":"MCO-BTC",
            "ctime":"2018-10-02	10:33:33",
            "type":"2",
            "side":"buy",
            "price":"0.123456",
            "number":"1.0000",
            "total_price":"0.123456",
            "deal_number":"0.00000",
            "deal_price":"0.00000",
            "status":1 17.
            }, ...
            }
        :param symbol: 如BTC_USDT 交易对
        :param type: 1=买入,2=卖出,不传即查全部
        :param fromid: 查询起始order_id  比如122
        :param direct: 查询方向(默认	prev)，prev	向前，时间（或	ID） 倒序；next	向后，时间（或	ID）正序）。（举例一 列数：1，2，3，4，5。from=4，prev有3，2，1； next只有5）
        :param limit: 分页返回的结果集数量，默认为20，最大为100
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/historyList'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        # args['data']['type'] = type
        args['data']['from'] = fromid
        args['data']['direct'] = direct
        args['data']['limit'] = limit

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def historyList2(self, symbol, limit):
        # 我的历史委托
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":	[{
            "order_id":121,
            "order_sn":"BL123456789987523",
            "symbol":"MCO-BTC",
            "ctime":"2018-10-02	10:33:33",
            "type":"2",
            "side":"buy",
            "price":"0.123456",
            "number":"1.0000",
            "total_price":"0.123456",
            "deal_number":"0.00000",
            "deal_price":"0.00000",
            "status":1 17.
            }, ...
            }
        :param symbol: 如BTC_USDT 交易对
        :param type: 1=买入,2=卖出,不传即查全部
        :param fromid: 查询起始order_id  比如122
        :param direct: 查询方向(默认	prev)，prev	向前，时间（或	ID） 倒序；next	向后，时间（或	ID）正序）。（举例一 列数：1，2，3，4，5。from=4，prev有3，2，1； next只有5）
        :param limit: 分页返回的结果集数量，默认为20，最大为100
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/historyList'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['symbol'] = symbol
        # args['data']['type'] = type
        # args['data']['from'] = fromid
        # args['data']['direct'] = direct
        args['data']['limit'] = limit

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def detail(self, order_sn):
        # 成交记录详情
        """
        {
        "errno":	0,
        "errmsg":	"success",
        "result":{
            "entrust":{
            "order_id":121,
            "order_sn":"BL123456789987523",
            "symbol":"MCO-BTC",
            "ctime":"2018-10-02	10:33:33",
            "type":"2",
            "side":"buy",
            "price":"0.123456",
            "number":"1.0000",
            "total_price":"0.123456",
            "deal_number":"0.00000",
            "deal_price":"0.00000",
            "status":1
            },
        }
        :param order_sn:订单编号
        :return:
        """
        args = dict()
        args['url'] = 'https://oapi.aofex.io/openApi/entrust/detail'
        args['method'] = 'GET'
        args['data'] = dict()
        args['data']['order_sn'] = order_sn

        result = await self.request(args)

        if result['code'] == 200:
            return json.loads(result['content'].decode('utf-8'))
        else:
            return result

    async def currentList4(self, symbol, number):
        current_list = []
        res_last = await self.currentList(symbol)
        print(res_last)
        if res_last.get('result', 0):
            length = len(res_last['result']) - 1
            last_id = res_last['result'][length]['order_sn']

            for i in res_last['result']:
                if i['status'] == 1 or i['status'] == 2:
                    current_list.append(i['order_sn'])
            flag = True
            while flag:
                start_id = last_id
                res = await self.currentList3(symbol, start_id, 'prev', 100)
                if len(res.get('result', 0)) == 1:
                    break
                if res.get('result', 0):
                    length = len(res['result']) - 1
                    last_id = res['result'][length]['order_sn']
                    for i in res['result']:

                        if i['status'] == 1 or i['status'] == 2:
                            if i['order_sn'] not in current_list:
                                current_list.append(i['order_sn'])
                    if len(current_list) >= number:
                        break
                else:
                    flag = False
            print(current_list)
            print('current_list: ', len(current_list))
            return current_list
        else:
            return current_list

    async def currentList4_order_details(self, symbol, number):
        current_list = []
        res_last = await self.currentList(symbol)

        if res_last.get('result', 0):
            length = len(res_last['result']) - 1
            last_id = res_last['result'][length]['order_sn']

            for i in res_last['result']:
                if i['status'] == 1 or i['status'] == 2:
                    current_list.append(i)
            flag = True
            while flag:
                start_id = last_id
                res = await self.currentList3(symbol, start_id, 'prev', 100)
                if len(res.get('result', 0)) == 1:
                    break
                if res.get('result', 0):
                    length = len(res['result']) - 1
                    last_id = res['result'][length]['order_sn']
                    for i in res['result']:

                        if i['status'] == 1 or i['status'] == 2:
                            if i['order_sn'] not in current_list:
                                current_list.append(i)
                    if len(current_list) >= number:
                        break
                else:
                    flag = False

            return current_list
        else:
            return current_list

    async def currentList5(self, symbol, number, side):
        current_list = []
        res_last = await self.currentList(symbol)
        # print(res_last)
        if res_last.get('result', 0):
            length = len(res_last['result']) - 1
            last_id = res_last['result'][length]['order_sn']

            for i in res_last['result']:
                if (i['status'] == 1 or i['status'] == 2) and i['side'] == side:
                    current_list.append(i['order_sn'])
                if (i['status'] == 1 or i['status'] == 2) and side is None:
                    current_list.append(i['order_sn'])
            flag = True
            while flag:
                start_id = last_id
                res = await self.currentList3(symbol, start_id, 'prev', 100)
                if len(res.get('result', [])) == 1:
                    break
                if res.get('result', 0):
                    length = len(res['result']) - 1
                    last_id = res['result'][length]['order_sn']
                    for i in res['result']:

                        if (i['status'] == 1 or i['status'] == 2) and i['side'] == side:
                            if i['order_sn'] not in current_list:
                                current_list.append(i['order_sn'])
                        if (i['status'] == 1 or i['status'] == 2) and side is None:
                            if i['order_sn'] not in current_list:
                                current_list.append(i['order_sn'])
                    if len(current_list) >= number:
                        break
                else:
                    flag = False
            # print(current_list)
            print('current_list: ', len(current_list))
            return current_list
        else:
            return current_list


if __name__ == '__main__':
    async def test():
        ao = AofexApi()
        price = await ao.newest_price('TVC-RLY')
        print(price)
        await ao.Exit()


    asyncio.run(test())
