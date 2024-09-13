#!/usr/bin/env ruby

# temporary until provider supports managing collaborators

require 'optparse'

options = {}

OptionParser.new do |parser|
  parser.banner = "Usage: heroku_add_access [options...]"
  parser.on("--app APP", "app") do |v|
    options[:app] = v
  end
  parser.on("--users USERS", "comma separated list of users") do |v|
    options[:users] = v
  end
  parser.on("--perms PERMS", "comma separated list of permissions") do |v|
    options[:perms] = v
  end
end.parse!

[:users, :perms].each do |option|
  if not options.include? option
    raise OptionParser::MissingArgument, option
  end
end

options[:users].split(',').each do |user|
  `heroku access:add #{user} -a #{options[:app]} --permissions #{options[:perms]}`
end
