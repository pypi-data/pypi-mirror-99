"""
    This file is part of TON OS.

    TON OS is free software: you can redistribute it and/or modify
    it under the terms of the Apache License 2.0 (http://www.apache.org/licenses/)

    Copyright 2019-2021 (c) TON LABS
"""

__version__ = '0.2.0rc0'

import sys
import base64, binascii
import secrets
import json
import numbers
import re
import copy
import os.path
import importlib
from glob import glob

PACKAGE_DIR = os.path.basename(os.path.dirname(__file__))
CORE = '.' + sys.platform + '.linker_lib'

try:
    core = importlib.import_module(CORE, PACKAGE_DIR)
except ImportError as err:
    print('Error: {}'.format(err))
    exit()
except:
    print('Unsupported platform:', sys.platform)
    exit()

QUEUE           = []
EVENTS          = []
ALL_MESSAGES    = []
NICKNAMES       = dict()

GRAM            = 1_000_000_000
EMPTY_CELL      = 'te6ccgEBAQEAAgAAAA=='

G_TESTS_PATH    = 'contracts/'

G_VERBOSE           = False
G_DUMP_MESSAGES     = False
G_STOP_AT_CRASH     = True
G_SHOW_EVENTS       = False
G_MSG_FILTER        = None
G_WARN_ON_UNEXPECTED_ANSWERS = False
G_STOP_ON_NO_ACCEPT = True

G_ABI_FIXER     = None

def version():
    return __version__

def reset_all():
    global QUEUE, EVENTS, ALL_MESSAGES, NICKNAMES
    core.reset_all()
    QUEUE           = []
    EVENTS          = []
    ALL_MESSAGES    = []
    NICKNAMES       = dict()


class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def green(msg):     return colorize(BColors.OKGREEN, str(msg))
def blue(msg):      return colorize(BColors.OKBLUE,  str(msg))
def red(msg):       return colorize(BColors.FAIL,    str(msg))
def yellow(msg):    return colorize(BColors.WARNING, str(msg))
def white(msg):     return colorize(BColors.BOLD,    str(msg))


class Msg:
    def __init__(self, data):
        assert isinstance(data, dict)
        # print(data)
        self.data       = data
        self.id         = data['id']
        if 'src' in data:
            self.src    = Address(data['src'])
        self.dst        = Address(data['dst'])
        self.type       = data['msg_type']
        self.timestamp  = data['timestamp']
        self.log_str    = data['log_str']

        if self.is_event():
            self.event  = data['name']

        if self.is_call() or self.is_answer():
            self.method = data['name']

        if not self.is_type('empty', 'unknown'):
            self.params  = data['params']

        self.value = None
        if not self.is_type('event', 'answer', 'external_call', 'call_getter'):
            self.value   = data['value']
            self.bounced = data['bounced']

    def is_type(self, type1, type2 = None, type3 = None, type4 = None, type5 = None):
        return self.type in [type1, type2, type3, type4, type5]
    def is_type_in(self, types):
        return self.type in types
    def is_answer(self, method = None):
        return self.is_type('answer') and (method is None or self.method == method)
    def is_call(self, method = None):
        return self.is_type('call') and (method is None or self.method == method)
    def is_empty(self):
        return self.is_type('empty')
    def is_event(self, e = None, src = None, dst = None):
        if self.is_type('event') and (e is None or self.event == e):
            if src is None or eq(src, self.src, msg = 'event.src:'):
                if dst is None or eq(dst, self.dst, msg = 'event.dst:'):
                    return True
        return False
    def is_unknown(self):
        return self.type == 'unknown'
    def dump_data(self):
        dump_struct(self.data)
    def __str__(self):
        return dump_struct_str(self.data)

class Address:
    """The :class:`Address <Address>` object, which contains an
    Address entity.
    """

    # Constructs `Address` object
    def __init__(self, addr):
        # addr: a string represented address or None
        if addr is None:
            addr = ''
        assert isinstance(addr, str), "{}".format(addr)
        if addr.startswith(':'):
            addr = '0' + addr
        # TODO: check that it is a correct address string
        self.addr_ = addr
    def __str__(self):
        # used by print()
        return 'Addr({})'.format(self.addr_)
    def __eq__(self, other):
        ensure_address(other)
        return self.str() == other.str()
    # Returns string representing given address
    def str(self):
        return self.addr_
    # Checks if address is empty
    def empty(self):            # TODO!!!: should this duplicate be removed?
        return self.str() == ''
    # Checks if address is none
    def is_none(self):
        return self.str() == ''
    # Adds workchain_id if it was missing
    def fix_wc(self):
        assert eq(':', self.addr_[0])
        self.addr_ = '0' + self.addr_
        return self

def zero_addr(wc):
    """Create a zero address instance.

    :param wc: Workchain ID.
    :return: :class:`Address <Address>` object
    :rtype: Address
    """

    addr = '{}:{}'.format(wc, '0'*64)
    return Address(addr)

def ensure_address(addr):
    """Validate given params against Address class.

    :param address: object of class Address
    """

    assert isinstance(addr, Address), red('Expected Address got {}'.format(addr))

class Bytes():
    def __init__(self, value):
        self.raw_ = value

    def __str__(self):
        return bytes2str(self.raw_)

    def __repr__(self):
        return "Bytes('{}')".format(self.raw_)

    def __eq__(self, other):
        if isinstance(other, Bytes):
            return self.raw_ == other.raw_
        elif isinstance(other, str):
            return str(self) == other
        return False


class JsonEncoder(json.JSONEncoder):
    def default(self, o):
        # verbose_(o)
        if isinstance(o, Address):
            return o.str()
        elif isinstance(o, Bytes):
            return o.raw_
        else:
            assert False

class Params:
    def __init__(self, params):
        assert isinstance(params, dict), '{}'.format(params)
        self.__raw__ = params
        self.transform(params)

    def transform(self, params):
        if isinstance(params, dict):
            for key in params:
                value = params[key]
                if isinstance(value, dict):
                    value = Params(value)
                if isinstance(value, Bytes):
                    value = str(value)
                if isinstance(value, list):
                    value = [self.tr(x) for x in value]
                setattr(self, key, value)

    def tr(self, x):
        if isinstance(x, dict):
            return Params(x)
        return x

def make_params(data):
    if isinstance(data, dict):
        return Params(data)
    if isinstance(data, list):
        return [make_params(x) for x in data]
    return data


# TODO: private
def transform_structure(value, callback):
    if isinstance(value, dict):
        nd = {}
        for key, v in value.items():
            nd[key] = transform_structure(v, callback)
        return nd
    if isinstance(value, list):
        return [transform_structure(x, callback) for x in value]
    return callback(value)

def fix_large_ints(v):
    def transform_value(v):
        if isinstance(v, Address):
            return v.str()
        if isinstance(v, Bytes):
            return v.raw_
        if isinstance(v, int):
            if v > 0xffffFFFFffffFFFF:
                v = hex(v)
            return v
        return v
    return transform_structure(v, transform_value)

def _json_dumps(j):
    j = fix_large_ints(j)
    return json.dumps(j) #, cls = JsonEncoder)


class ExecutionResult:
    def __init__(self, result):
        (ec, actions, gas, err) = result
        self.exit_code  = ec
        self.actions    = actions
        self.gas_used   = gas
        self.error      = err


def init(path, verbose = False, time = None):
    # TODO correct the description for Sphinx
    """Init library.
    :param path: set a directory where the artifacts of the used contracts are located
    :param verbose: toggle to print additional execution info
    :param time: in seconds. TS4 uses either real-clock or virtual time. Once you set time you switch
    """

    script_path = os.path.dirname(sys.argv[0])
    path = os.path.join(
        script_path if not os.path.isabs(path) else '',
        path
    )
    set_tests_path(path)
    set_verbose(verbose)
    if time is not None:
        core.set_now(time)

def set_verbose(f):
    global G_VERBOSE
    G_VERBOSE = f

def set_stop_at_crash(f):
    global G_STOP_AT_CRASH
    G_STOP_AT_CRASH = f

def verbose_(msg):
    verbose(msg, show_always = True, color_red = True)

def verbose(msg, show_always = False, color_red = False):
    if G_VERBOSE or show_always:
        if color_red:
            msg = red(str(msg))
        print(msg)

def prettify_dict(d, max_str_len = 67):
    nd = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nd[k] = prettify_dict(v, max_str_len = max_str_len)
        elif isinstance(v, str):
            nd[k] = v if len(v) <= max_str_len else v[:max_str_len] + '...'
        elif isinstance(v, Address):
            nd[k] = _format_addr(v, compact = False)
        else:
            nd[k] = v

    return nd

def process_actions(result: ExecutionResult, expect_ec = 0):
    assert isinstance(result, ExecutionResult)
    ec = result.exit_code

    if G_VERBOSE:
        if ec != 0:
            print(yellow('exit_code = {}'.format(ec)))

    assert eq(expect_ec, ec, dismiss = not G_STOP_AT_CRASH)
    assert eq(None, result.error)

    answer = None

    for j in result.actions:
        msg = Msg(json.loads(j))
        # if G_VERBOSE:
            # print('process msg:', msg)
        if msg.is_event():
            if G_VERBOSE or G_SHOW_EVENTS:
                xtra = ''
                params = msg.params
                if msg.is_event('DebugEvent'):
                    xtra = ' ={}'.format(decode_int(params['x']))
                elif msg.is_event('LogEvent'):
                    params['comment'] = bytearray.fromhex(params['comment']).decode()
                print(yellow("{} {}{}".format(msg.event, params, xtra)))
            EVENTS.append(msg)
        else:
            # not event
            if msg.is_unknown():
                if G_VERBOSE:
                    print(yellow('WARNING! Unknown message!'))
            elif msg.is_answer():
                # We expect only one answer
                assert answer is None
                answer = msg
                continue
            # elif G_WARN_ON_UNEXPECTED_ANSWERS and msg.is_answer():
                # verbose_('WARNING! Unexpected answer!')
                # continue
            else:
                assert msg.is_call() or msg.is_empty(), red('Unexpected type: {}'.format(msg.type))
            QUEUE.append(msg)
    return (result.gas_used, answer)

def pop_msg():
    assert len(QUEUE) > 0
    return QUEUE.pop(0)

def peek_msg():
    assert len(QUEUE) > 0
    return QUEUE[0]

def pop_event():
    assert len(EVENTS) > 0
    return EVENTS.pop(0)

def peek_event():
    assert len(EVENTS) > 0
    return EVENTS[0]

def queue_length():
    return len(QUEUE)

def ensure_queue_empty():
    assert eq(0, len(QUEUE), msg = ('ensure_queue_empty() -'))

def dump_queue():
    print(colorize(BColors.BOLD, "QUEUE:"))
    for i in range(len(QUEUE)):
        print("  {}: {}".format(i, QUEUE[i]))

def dispatch_messages():
    while len(QUEUE) > 0:
        dispatch_one_message()

def dump_all_messages():
    prev_time = 0
    for msg in ALL_MESSAGES:
        cur_time = msg['timestamp']
        if cur_time == prev_time:
            print('---------------')
        else:
            print('--------------- {} ------------ ------------ ------------'
                .format(colorize(BColors.BOLD, str(cur_time))))
            prev_time = cur_time
        dump_message(msg)

def register_nickname(addr, nickname):
    ensure_address(addr)
    NICKNAMES[addr.str()] = nickname

def _format_addr(addr, compact = True):
    ensure_address(addr)
    if addr.empty():
        return 'addr_none'
    addr = addr.str()
    s = addr[:10]
    if addr in NICKNAMES:
        s = "{} ({})".format(NICKNAMES[addr], s)
    else:
        if not compact:
            s = 'Addr({})'.format(s)
    return s

def dump_message(msg: Msg):
    assert isinstance(msg, Msg)
    value = msg.value / GRAM if msg.value is not None else 'n/a'
    # print(msg)
    print(yellow('> {} -> {}'.format(
        _format_addr(msg.src),
        _format_addr(msg.dst)
    )) + ', v: {}'.format(value))
    if msg.is_type('call',  'empty'):
        # ttt = "{}".format(msg)
        if msg.is_call():
            ttt = "{} {}".format(green(msg.method), msg.params)
        else:
            ttt = green('<empty>')
        print("> " + ttt)
    elif msg.is_unknown():
        ttt = green('<unknown>')
        print("> " + ttt)
    else:
        assert msg.is_answer()
        ttt = '{}'.format(msg.data)
        print("> " + green(ttt))

def dispatch_one_message(expect_ec = 0):
    msg = pop_msg()
    ALL_MESSAGES.append(msg)
    # if is_method_call(msg, 'onRoundComplete'):
        # dump_message(msg)
    dump1 = G_VERBOSE or G_DUMP_MESSAGES
    dump2 = G_MSG_FILTER is not None and G_MSG_FILTER(msg.data)
    if dump1 or dump2:
        dump_message(msg)
    if msg.dst.empty():
        # TODO: a getter's reply. Add a test for that
        return
    # if msg['id'] == 2050: core.set_trace(True)
    result = core.dispatch_message(msg.id)
    result = ExecutionResult(result)
    gas, answer = process_actions(result, expect_ec)
    assert answer is None
    # if msg['id'] == 2050: quit()
    return gas

def set_msg_filter(filter):
    global G_MSG_FILTER
    if filter is True:  filter = lambda msg: True
    if filter is False: filter = None
    G_MSG_FILTER = filter

def decode_int(v):
    if v[0:2] == '0x':
        return int(v.replace('0x', ''), 16)
    else:
        return int(v)

class DecodingParams:
    def __init__(self,
        decode_ints = True,
        decode_tuples = True,
        dont_decode_fields = [],
    ):
        self.decode_ints = decode_ints
        self.decode_tuples = decode_tuples
        self.dont_decode_fields = dont_decode_fields

def decode_json_value1(value, full_type, params):
    type = full_type['type']

    if re.match(r'^(u)?int\d+$', type):
        return decode_int(value) if params.decode_ints else value

    if type[-2:] == '[]':
        type2 = copy.deepcopy(full_type)
        type2['type'] = type[:-2]
        res = []
        for v in value:
            res.append(decode_json_value1(v, type2, params))
        return res

    if type == 'bool':
        return bool(value)

    if type == 'address':
        return Address(value)

    if type == 'cell':
        return value
        
    if type == 'bytes':
        return Bytes(value)

    if type == 'tuple':
        assert isinstance(value, dict)
        res = {}
        for c in full_type['components']:
            field = c['name']
            dont_decode = 'dont_decode' in c
            if dont_decode or field in params.dont_decode_fields:
                res[field] = value[field]
            else:
                res[field] = decode_json_value1(value[field], c, params)
        return res

    print(type, full_type, value)
    verbose_("Unsupported type '{}'".format(type))
    return value

def make_keypair():
    (secret_key, public_key) = core.make_keypair()
    public_key = '0x' + public_key
    return (secret_key, public_key)

def colorize(color, text):
    if sys.stdout.isatty():
        return color + text + BColors.ENDC
    else:
        return text

def eq(v1, v2, dismiss = False, msg = None, xtra = ''):
    if v1 == v2:
        return True
    else:
        if msg is None:
            msg = ''
        else:
            msg = msg + ' '
        print(msg + red('exp: {}, got: {}.'.format(v1, v2)) + xtra)
        return True if dismiss else False

def set_tests_path(path):
    global G_TESTS_PATH
    G_TESTS_PATH = path

def str2bytes(s: str) -> str:
    assert isinstance(s, str), 'Expected string got {}'.format(s)
    ss = str(binascii.hexlify(s.encode()))[1:]
    return ss.replace("'", "")

def bytes2str(b: str) -> str:
    return binascii.unhexlify(b).decode('utf-8')

def make_secret_token(n):
    return '0x' + secrets.token_hex(n)

def fix_uint256(s):
    assert s[0:2] == '0x', 'Expected hexadecimal, got {}'.format(s)
    t = s[2:]
    if len(t) < 64:
        s = '0x' + ('0' * (64-len(t))) + t
    return s

def dump_struct_str(struct):
    return json.dumps(struct, indent = 2, cls = JsonEncoder)

def dump_struct(struct, compact = False):
    if compact:
        print(json.dumps(struct))
    else:
        print(dump_struct_str(struct))

def load_tvc(fn):
    fn = os.path.join(G_TESTS_PATH, fn)
    if not fn.endswith('.tvc'):
        fn += '.tvc'
    bytes = open(fn, 'rb').read(1_000_000)
    return base64.b64encode(bytes).decode('utf-8')

def load_code_cell(fn):
    fn = os.path.join(G_TESTS_PATH, fn)
    if not fn.endswith('.tvc'):
        fn += '.tvc'
    return core.load_code_cell(fn)

def load_data_cell(fn):
    fn = os.path.join(G_TESTS_PATH, fn)
    if not fn.endswith('.tvc'):
        fn += '.tvc'
    return core.load_data_cell(fn)

def grams(n):
    return '{:.3f}'.format(n / GRAM).replace('.000', '')

def ensure_balance(expected, got, dismiss = False, epsilon = 0, msg = None):
    diff = got - int(expected)
    if abs(diff) <= epsilon:
        return
    xtra = ", diff = {}g ({})".format(grams(diff), diff)
    assert eq(int(expected), got, xtra = xtra, dismiss = dismiss, msg = msg)

def register_abi(contract_name):
    fn = os.path.join(G_TESTS_PATH, contract_name) + '.abi.json'
    if G_VERBOSE:
        print(blue("Loading ABI " + fn))
    core.set_contract_abi(None, fn)

def set_contract_abi(contract, new_abi_name):
    assert isinstance(contract, BaseContract)
    fn = os.path.join(G_TESTS_PATH, new_abi_name)
    if not fn.endswith('.abi.json'):
        fn += '.abi.json'
    core.set_contract_abi(contract.addr().str(), fn)
    contract.abi_ = json.loads(open(fn).read())


#########################################################################################################

def dump_js_data():
    all_runs = get_all_runs()
    msgs = get_all_messages()
    with open('msg_data.js', 'w') as f:
        print('var allMessages = ' + dump_struct_str(msgs) + ';', file = f)
        print('var nicknames = ' + dump_struct_str(NICKNAMES) + ';', file = f)
        print('var allRuns = ' + dump_struct_str(all_runs) + ';', file = f)

def get_all_runs():
    return json.loads(core.get_all_runs())

def get_all_messages(show_all = False):
    def filter(msg):
        msg = Msg(msg)
        # TODO: support getters/answers
        assert isinstance(msg, Msg), "{}".format(msg)
        if show_all:
            return True
        return msg.is_type_in(['call', 'external_call', 'empty', 'event', 'unknown', 'log'])
    msgs = json.loads(core.get_all_messages())
    return [m for m in msgs if filter(m)]

#########################################################################################################

# TODO: is it needed here?
class BalanceWatcher:
    def __init__(self, contract):
        self.contract_  = contract
        self.balance_   = contract.balance()
        self.epsilon_   = 2
    def ensure_change(self, expected_diff):
        cur_balance     = self.contract_.balance()
        prev_balance    = self.balance_
        ensure_balance(prev_balance + expected_diff, cur_balance, epsilon = self.epsilon_)
        self.balance_   = cur_balance


#########################################################################################################

class AbiTraversalHelper:
    def __init__(self, abi_name, abi_json):
        self.name_ = abi_name
        self.json_ = abi_json

    def travel_fields(self, cb):
        for f in self.json_['functions']:
            self.recFunc(self.name_ + '.functions', f, cb)
        for e in self.json_['events']:
            self.recEvent(self.name_ + '.events', e, cb)

    def recFunc(self, path, json, cb):
        path = path + '.' + json['name']
        # print(path)
        for j in json['outputs']:
            self.recVar(path + '.outputs', j, cb)

    def recEvent(self, path, json, cb):
        path = path + '.' + json['name']
        # print(path)
        for j in json['inputs']:
            self.recVar(path + '.inputs', j, cb) # TODO: do we need inputs here?

    def recVar(self, path, json, cb):
        path = path + '.' + json['name']
        type = json['type']
        while type.endswith('[]'):
            type = type[:len(type)-2]
        # print(path, type)
        if type == 'tuple':
            for j in json['components']:
                self.recVar(path, j, cb)
        cb(path, json)

def fix_abi(name, abi, callback):
    """Travels given ABI calling a callback function for each node
    :param name: contract name
    :param abi: contract abi
    :param callback: transformation function called for each node.
    """
    traveller = AbiTraversalHelper(name, abi)
    traveller.travel_fields(callback)


#########################################################################################################

def get_balance(addr):
    ensure_address(addr)
    return core.get_balance(addr.str())

# A class responsible for deploying contracts and interaction with deployed contracts.
class BaseContract:
    def init2(self, name, address, nickname = None, just_deployed = False):
        self.name_ = name
        ensure_address(address)
        self.addr_ = address
        name = os.path.join(G_TESTS_PATH, name)
        if not just_deployed:
            if G_VERBOSE:
                print(colorize(BColors.OKBLUE, 'Creating wrapper for ' + name))
            core.set_contract_abi(self.address().str(), name + '.abi.json')

        # Load ABI
        self.abi_ = json.loads(open(name + '.abi.json').read())

        if G_ABI_FIXER is not None:
            fix_abi(self.name_, self.abi_, G_ABI_FIXER)

    # Retreives balance of a given contract
    def balance(self):
        return get_balance(self.address())

    # Returns address of a given contact
    def address(self):
        return self.addr_

    # Returns address of a given contact
    def addr(self):
        return self.addr_

    def ensure_balance(self, v, dismiss = False):
        # TODO: is this method needed here?
        ensure_balance(v, self.balance(), dismiss)

    # Calls a given getter and returns an answer in raw JSON format
    def call_getter_raw(self, method, params = dict(), expect_ec = 0):
        # method: name of a getter
        # params: a dictionary with getter parameters
        # expect_ec: expected exit code. Use non-zero value if you expect a getter to raise an exception
        if G_VERBOSE:
            print('getter: {}'.format(green(method)))   # TODO!: print full info
            # print("getter: {} {}".format(method, params))

        assert isinstance(method,    str)
        assert isinstance(params,    dict)
        assert isinstance(expect_ec, int)

        result = core.call_contract(
            self.addr().str(),
            method,
            True,   # is_getter
            _json_dumps(params),
            None,   # private_key
        )

        result = ExecutionResult(result)
        assert eq(None, result.error)
        # print(actions)
        assert eq(expect_ec, result.exit_code)

        if expect_ec != 0:
            return

        actions = [Msg(json.loads(a)) for a in result.actions]

        for msg in actions:
            if not msg.is_answer():
                raise Exception("Unexpected message type '{}' in getter output".format(msg.type))

        assert eq(1, len(result.actions)), 'len(actions) == 1'
        msg = Msg(json.loads(result.actions[0]))
        assert msg.is_answer(method)
        return msg.params

    def _find_getter_output_types(self, method):
        for rec in self.abi_['functions']:
            if rec['name'] == method:
                return rec['outputs']
        assert False

    def _find_getter_output_type(self, method, key):
        types = self._find_getter_output_types(method)
        for t in types:
            if t['name'] == key:
                return t
        assert False

    # Calls a given getter and decodes an answer
    def call_getter(self,
        method,
        params = dict(),
        key = None,
        decode_ints = True,     # TODO: remove!
        decode_tuples = True,   # TODO: remove!
        dont_decode_fields = [],    # TODO: maybe remove?
        expect_ec = 0,
        decode = False,
    ):
        # method: name of a getter
        # params: a dictionary with getter parameters
        # expect_ec: expected exit code. Use non-zero value if you expect a getter to raise an exception
        # dont_decode_fields: a list of fields in answer that should not be decoded
        # returns: a returned value in decoded form (exact type depends on the type of getter)

        values = self.call_getter_raw(method, params, expect_ec)

        if expect_ec > 0:
            # TODO: ensure values is empty?
            return

        answer = self._decode_answer(values, method, key, DecodingParams(decode_ints, decode_tuples, dont_decode_fields))
        return make_params(answer) if decode else answer

    def _decode_answer(self,
        values,
        method,
        key,
        params,
    ):

        keys = list(values.keys())

        if key is None and len(keys) == 1:
            key = keys[0]

        if key is None:
            return self._make_tuple_result(method, values, params)

        assert key is not None
        assert key in values, red("No '{}' in {}".format(key, values))

        value     = values[key]
        full_type = self._find_getter_output_type(method, key)

        return decode_json_value1(value, full_type, params)

    # Experimental feature
    def decode_event(self, event_msg):
        assert isinstance(event_msg, Msg), '{}'.format(event_msg)

        values      =   event_msg.data['params']
        event_name  =   event_msg.event
        event_def   =   self._find_event_def(event_name)

        assert event_def is not None, red('Cannot find event: {}'.format(event_name))

        # TODO!!: copy/paste - refactor!
        res = {}
        for type in event_def['inputs']:
            # TODO!: Add class for Type
            name  = type['name']
            value = values[name]
            if 'dont_decode' not in type:
                params = DecodingParams()
                value = decode_json_value1(value, type, params)
            res[name] = value

        return res

    def _dump_event_type(self, msg):
        assert msg.is_event()
        dump_struct(self._find_event_def(msg.event))

    def _find_event_def(self, event_name):
        assert isinstance(event_name, str)
        for event_def in self.abi_['events']:
            if event_def['name'] == event_name:
                return event_def
        return None

    def _make_tuple_result(self, method, values, params):
        types = self._find_getter_output_types(method)
        res_dict = {}
        res_arr  = []
        for type in types:
            # TODO!: Add class for Type
            name  = type['name']
            value = decode_json_value1(values[name], type, params)
            res_dict[name] = value
            res_arr.append(value)
        if params.decode_tuples and types[0]['name'] == 'value0':
            return tuple(res_arr)
        else:
            return res_dict

    # Calls a given method.
    def call_method(self, method, params = dict(), private_key = None, expect_ec = 0):
        # method: name of a method to be called
        # params: a dictionary with parameters
        # expect_ec: expected exit code. Use non-zero value if you expect a getter to raise an exception
        # private_key: a private key to be used to sign a message
        # returns: a returned value in decoded form (if method returns something)

        # TODO: check param types. In particular, that `private_key` looks correct.
        #       Or introduce special type for keys...
        assert isinstance(params, dict)
        if G_VERBOSE:
            print(green("{} {}".format(method, prettify_dict(params))))
        try:
            result = core.call_contract(
                self.addr().str(),
                method,
                False, # is_getter
                _json_dumps(params),
                private_key,
            )
            result = ExecutionResult(result)
        except:
            print(_json_dumps(params))
            raise

        if result.error == 'no_accept':
            severity = 'ERROR' if G_STOP_ON_NO_ACCEPT else 'WARNING'
            err_msg = '{}! No ACCEPT in the contract method `{}`'.format(severity, method)
            assert not G_STOP_ON_NO_ACCEPT, err_msg
            verbose_(err_msg)
        else:
            _gas, answer = process_actions(result, expect_ec)
            if answer is not None:
                assert answer.is_answer(method)
                key = None
                return self._decode_answer(answer.params, method, key, DecodingParams())

    # Calls a given method using contract's private key
    def call_method_signed(self, method, params = dict(), expect_ec = 0):
        self.call_method(method, params, private_key = self.private_key_, expect_ec = expect_ec)

    # Simulates tick-tick call
    def ticktock(self, is_tock):
        # is_tock: Boolean: False for Tick and True for Tock
        if G_VERBOSE:
            print('ticktock {}'.format(_format_addr(self.address())))
        result = core.call_ticktock(self.address().str(), is_tock)
        result = ExecutionResult(result)
        gas, answer = process_actions(result)
        assert answer is None
        return gas

    # Creates new keypair and assigns it to the contract
    def create_keypair(self):
        (self.private_key_, self.public_key_) = make_keypair()

    # Returns keypair assigned to the contract
    def keypair(self):
        return (self.private_key_, self.public_key_)

    # Constructs BaseContract class
    def __init__(self,
        name,               # name used to load contract's bytecode and ABI
        ctor_params,        # parameters for offchain constructor call. If None constructor is not called and 
                            # can be called with separate `call_method()` call (onchain constructed)
        wc = 0,             # workchain_id to deploy contract to
        address             = None,     # if this parameter is specified no new contract is created
                                        # but instead a wrapper for an existing contract is created.
        override_address    = None,     # when specified this address will be used for deploying the contract
                                        # otherwise the address is generated according real blockchain rules.
        pubkey              = None,         # public key used in contract construction.
        private_key         = None,         # private key used to sign construction message.
        balance             = 100 * GRAM,       # desired contract balance
        nickname            = None,         # nickname of a contract used in verbose output
    ):
        full_name = os.path.join(G_TESTS_PATH, name)
        just_deployed = False
        if override_address is not None:
            ensure_address(override_address)
            override_address = override_address.str()
        if address is None:
            if G_VERBOSE:
                print(blue('Deploying {} ({})'.format(full_name, nickname)))
            if pubkey is not None:
                assert pubkey[0:2] == '0x'
                pubkey = pubkey.replace('0x', '')
            address = core.deploy_contract(
                full_name + '.tvc',
                full_name + '.abi.json',
                _json_dumps(ctor_params) if ctor_params is not None else None,
                pubkey,
                private_key,
                wc,
                override_address,
                balance,
            )
            address = Address(address)
            just_deployed = True
        self.init2(name, address, just_deployed = just_deployed)
        if nickname is not None:
            register_nickname(self.address(), nickname)

