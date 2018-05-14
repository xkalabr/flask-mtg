from marshmallow import Schema, fields, post_load


class Inventory():
  def __init__(self, cid, price, cond, indeck, isfoil):
    self.cid = cid
    self.price = price
    self.cond = cond
    self.indeck = indeck
    self.isfoil = isfoil

  def __repr__(self):
    return '<Inventory(cid={self.cid!r})>'.format(self=self)


class InventorySchema(Schema):
  cid = fields.Str()
  price = fields.Str()
  cond = fields.Number()
  indeck = fields.Boolean()
  isfoil = fields.Boolean()

  @post_load
  def make_card(self, data):
    return Inventory(**data)
