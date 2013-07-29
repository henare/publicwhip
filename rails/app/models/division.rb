class Division < ActiveRecord::Base
  self.table_name = "pw_division"

  has_one :division_info

  delegate :rebellions, :turnout, :aye_majority, to: :division_info
  alias_attribute :date, :division_date
  alias_attribute :name, :division_name
  alias_attribute :number, :division_number

  def division_name
    # For some reason some characters are stored in the database using html entities
    # rather than using unicode.
    HTMLEntities.new.decode(read_attribute(:division_name))
  end

  # This is a bit of a guess
  def majority
    aye_majority.abs
  end

  def clock_time
    text = read_attribute(:clock_time)
    Time.parse(text) if text && text != ""
  end

  def australian_house
    case house
    when "commons"
      "representatives"
    when "lords"
      "senate"
    else
      raise "Unexpected value"
    end
  end

  def australian_house_name
    case house
    when "commons"
      "Representatives"
    when "lords"
      "Senate"
    else
      raise "Unexpected value"
    end
  end
end
