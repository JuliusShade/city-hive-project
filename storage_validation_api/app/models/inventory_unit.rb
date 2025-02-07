class InventoryUnit
  include Mongoid::Document
  include Mongoid::Timestamps  # Adds created_at and updated_at automatically

  field :item_num, type: String
  field :name, type: String
  field :price, type: Float
  field :department, type: String
  field :properties, type: Hash  # Stores department, vendor, and description
  field :tags, type: Array, default: []
  field :batch_id, type: String  # Shared batch identifier for API calls
end
