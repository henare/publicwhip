class House
  def self.uk_to_australian(house)
    case house
    when "commons"
      "representatives"
    when "lords"
      "senate"
    else
      raise "Unexpected value"
    end
  end

  def self.australian_to_uk(australian_house)
    case australian_house
    when "representatives"
      "commons"
    when "senate"
      "lords"
    else
      raise "unexpected value"
    end
  end
end