# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: client.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63lient.proto\"\"\n\x0fServeClientArgs\x12\x0f\n\x07Request\x18\x01 \x01(\t\"C\n\x10ServeClientReply\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\t\x12\x10\n\x08LeaderID\x18\x02 \x01(\t\x12\x0f\n\x07Success\x18\x03 \x01(\x08\x32\x43\n\rClientService\x12\x32\n\x0bServeClient\x12\x10.ServeClientArgs\x1a\x11.ServeClientReplyb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'client_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SERVECLIENTARGS']._serialized_start=16
  _globals['_SERVECLIENTARGS']._serialized_end=50
  _globals['_SERVECLIENTREPLY']._serialized_start=52
  _globals['_SERVECLIENTREPLY']._serialized_end=119
  _globals['_CLIENTSERVICE']._serialized_start=121
  _globals['_CLIENTSERVICE']._serialized_end=188
# @@protoc_insertion_point(module_scope)
