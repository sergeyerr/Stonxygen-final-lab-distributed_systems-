# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Finance_API.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='Finance_API.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11\x46inance_API.proto\"2\n\x05Stock\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x03(\x01\"\x1c\n\x0bStock_Codes\x12\r\n\x05\x63odes\x18\x01 \x01(\t\"\x14\n\x12Get_stocks_request2m\n\x0cStocksLoader\x12-\n\nget_stocks\x12\x13.Get_stocks_request\x1a\x06.Stock\"\x00\x30\x01\x12.\n\x12get_stocks_history\x12\x0c.Stock_Codes\x1a\x06.Stock\"\x00\x30\x01\x62\x06proto3'
)




_STOCK = _descriptor.Descriptor(
  name='Stock',
  full_name='Stock',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Stock.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code', full_name='Stock.code', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='price', full_name='Stock.price', index=2,
      number=3, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=71,
)


_STOCK_CODES = _descriptor.Descriptor(
  name='Stock_Codes',
  full_name='Stock_Codes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='codes', full_name='Stock_Codes.codes', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=73,
  serialized_end=101,
)


_GET_STOCKS_REQUEST = _descriptor.Descriptor(
  name='Get_stocks_request',
  full_name='Get_stocks_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=103,
  serialized_end=123,
)

DESCRIPTOR.message_types_by_name['Stock'] = _STOCK
DESCRIPTOR.message_types_by_name['Stock_Codes'] = _STOCK_CODES
DESCRIPTOR.message_types_by_name['Get_stocks_request'] = _GET_STOCKS_REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Stock = _reflection.GeneratedProtocolMessageType('Stock', (_message.Message,), {
  'DESCRIPTOR' : _STOCK,
  '__module__' : 'Finance_API_pb2'
  # @@protoc_insertion_point(class_scope:Stock)
  })
_sym_db.RegisterMessage(Stock)

Stock_Codes = _reflection.GeneratedProtocolMessageType('Stock_Codes', (_message.Message,), {
  'DESCRIPTOR' : _STOCK_CODES,
  '__module__' : 'Finance_API_pb2'
  # @@protoc_insertion_point(class_scope:Stock_Codes)
  })
_sym_db.RegisterMessage(Stock_Codes)

Get_stocks_request = _reflection.GeneratedProtocolMessageType('Get_stocks_request', (_message.Message,), {
  'DESCRIPTOR' : _GET_STOCKS_REQUEST,
  '__module__' : 'Finance_API_pb2'
  # @@protoc_insertion_point(class_scope:Get_stocks_request)
  })
_sym_db.RegisterMessage(Get_stocks_request)



_STOCKSLOADER = _descriptor.ServiceDescriptor(
  name='StocksLoader',
  full_name='StocksLoader',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=125,
  serialized_end=234,
  methods=[
  _descriptor.MethodDescriptor(
    name='get_stocks',
    full_name='StocksLoader.get_stocks',
    index=0,
    containing_service=None,
    input_type=_GET_STOCKS_REQUEST,
    output_type=_STOCK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='get_stocks_history',
    full_name='StocksLoader.get_stocks_history',
    index=1,
    containing_service=None,
    input_type=_STOCK_CODES,
    output_type=_STOCK,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_STOCKSLOADER)

DESCRIPTOR.services_by_name['StocksLoader'] = _STOCKSLOADER

# @@protoc_insertion_point(module_scope)