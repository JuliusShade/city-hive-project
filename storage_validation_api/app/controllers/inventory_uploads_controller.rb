class InventoryUploadsController < ApplicationController
    # POST /inventory_uploads.json
    def create
      batch_id = SecureRandom.uuid  # Generate a unique batch_id
      inventory_units = []
  
      params[:inventory_units].each do |unit|
        inventory_units << InventoryUnit.new(
          item_num: unit[:item_num],
          name: unit[:name],
          price: unit[:price],
          department: unit[:department],
          properties: unit[:properties],
          tags: unit[:tags],
          batch_id: batch_id
        )
      end
  
      if InventoryUnit.collection.insert_many(inventory_units.map(&:attributes))
        render json: { message: "Inventory uploaded successfully", batch_id: batch_id }, status: :created
      else
        render json: { error: "Failed to upload inventory" }, status: :unprocessable_entity
      end
    end
  
    # GET /inventory_uploads.json
    def index
      summary = InventoryUnit.collection.aggregate([
        { "$group": {
          "_id": "$batch_id",
          "number_of_units": { "$sum": 1 },
          "average_price": { "$avg": "$price" },
          "total_quantity": { "$sum": "$properties.quantity" }
        }},
        { "$project": {
          "_id": 0,
          "batch_id": "$_id",
          "number_of_units": 1,
          "average_price": 1,
          "total_quantity": 1
        }}
      ]).to_a
  
      render json: summary, status: :ok
    end
  end
  