class Stock
  def initialize(code, organization, price)
    @code = code
    @organization = organization
    @price = price
  end

  def self.all_available
  end

  def to_json(*options)
    {
      code: @code,
      organization: @organization,
      price: @price
    }.to_json(*options)
  end
end
