#!/usr/bin/ruby
# coding: utf-8

puts $$
pid = fork()

if pid.nil?
  puts "Soy el proceso hijo. Mi PID es #{$$}"
else
  puts "Soy el proceso padre. Mi PID es #{$$}. El del hijo es #{pid}."
  Process.wait(pid)
  system('ps ax | less')
end

